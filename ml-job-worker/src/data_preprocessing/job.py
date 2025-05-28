from celery import shared_task

from src.common.clients import JobHttpxAPI
from src.common.dto import JobStartDTO
from src.common.serializers import JobEndSerializer
from src.common.types import (
    JobEndActionType,
    JobType,
)
from src.common.utils import (
    get_current_utc_datetime,
    get_error_log,
    get_norm_path,
    read_config_file,
    write_log_file,
)
from src.data_preprocessing.config import DataPreprocessingConfig
from src.data_preprocessing.utils import run
from src.infrastructure.clients import api_client
from src.infrastructure.storages import (
    lfs_files_dir_path,
    lfs_spectra_dir_path,
)


@shared_task(bind=True, pydantic=True, name=JobType.DATA_PREPROCESSING)
def data_preprocessing_job(self, dto: JobStartDTO) -> None:
    """
    Celery task to run the data preprocessing pipeline for a given Data Preprocessing job.

    This task will:
      1. Construct absolute paths for the job’s config.json, result.h5, and log.txt under the shared filesystem.
      2. Read and validate the JSON config into a DataPreprocessingConfig.
      3. Normalize the raw spectra directory path and assign the output HDF5 path.
      4. Invoke the `run` helper to interpolate and scale spectra, then write the HDF5.
      5. Report success or failure back to the ML Job API via JobHttpxAPI.
      6. Write a log file capturing success, manual abort, or error stack trace.

    Parameters:
        self: Bound task instance, exposing `.request.id` as the job UUID.
        dto (JobStartDTO): DTO containing `dir_path` where config.json lives.
    """

    job_id = self.request.id
    job_api = JobHttpxAPI(api_client)

    #

    # Build absolute paths for config, result, and log files under LFS
    config_file_path = get_norm_path(dto.dir_path, prefix=lfs_files_dir_path, child_name="config.json")
    result_file_path = get_norm_path(dto.dir_path, prefix=lfs_files_dir_path, child_name="result.h5")
    log_file_path = get_norm_path(dto.dir_path, prefix=lfs_files_dir_path, child_name="log.txt")

    #

    log = None
    started_at = get_current_utc_datetime()

    try:
        # Load Data Preprocessing configuration
        config_file_data = read_config_file(config_file_path)

        # Validate Data Preprocessing configuration
        config = DataPreprocessingConfig.model_validate(config_file_data)
        config.data_dir_path = get_norm_path(config.data_dir_path, prefix=lfs_spectra_dir_path)
        config.result_file_path = result_file_path

        # Execute the preprocessing pipeline
        run(config)

        #

        # On success, notify the API
        log = "Job was successfully processed!"
        ended_at = get_current_utc_datetime()

        job_api.end_job_by_job_id_and_job_end_action(
            job_id, JobEndActionType.COMPLETE, JobEndSerializer(started_at=started_at, ended_at=ended_at)
        )

    except SystemExit:
        # Manual abort (e.g. SIGTERM) recorded as user abort
        log = "Job was manually aborted!"

    except Exception:
        # Any other exception: capture stack trace, notify API of error
        log = get_error_log()
        ended_at = get_current_utc_datetime()

        job_api.end_job_by_job_id_and_job_end_action(
            job_id, JobEndActionType.ERROR, JobEndSerializer(started_at=started_at, ended_at=ended_at)
        )

    finally:
        # Always write out the task log
        write_log_file(log_file_path, log)
