import time

from celery import shared_task

from src.active_ml.clients import LabellingHttpxAPI
from src.active_ml.serializers import LabellingInitializeSerializer
from src.active_ml.types import LabellingSpectrumSetType
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
from src.infrastructure.clients import api_client
from src.infrastructure.storages import (
    lfs_files_dir_path,
)
from src.active_ml.config import ActiveLearningConfig
from src.active_ml.iterations import (
    zero_iteration,
    regular_iteration
)

@shared_task(bind=True, pydantic=True, name=JobType.ACTIVE_ML)
def active_ml_job(self, dto: JobStartDTO) -> None:
    job_id = self.request.id
    job_api = JobHttpxAPI(api_client)
    labelling_api = LabellingHttpxAPI(api_client)

    #

    config_file_path = get_norm_path(dto.dir_path, prefix=lfs_files_dir_path, child_name="config.json")
    result_dir_path = get_norm_path(dto.dir_path, prefix=lfs_files_dir_path)
    log_file_path = get_norm_path(dto.dir_path, prefix=lfs_files_dir_path, child_name="log.txt")

    log = None
    started_at = get_current_utc_datetime()

    #

    try:
        config_file_data = read_config_file(config_file_path)
        config = ActiveLearningConfig.model_validate(config_file_data)
        config.result_dir_path = result_dir_path

        if config.training_data_path:
            config.training_data_path = get_norm_path(config.training_data_path, prefix=lfs_files_dir_path)
        
        if config.pool_data_path:
            config.pool_data_path = get_norm_path(config.pool_data_path, prefix=lfs_files_dir_path)

        if config.training_data_to_add_path:
            config.training_data_to_add_path = get_norm_path(config.training_data_to_add_path, prefix=lfs_files_dir_path)

        if config.oracle_data_to_add_path:
            config.oracle_data_to_add_path = get_norm_path(config.oracle_data_to_add_path, prefix=lfs_files_dir_path)

        if config.perf_est_list_path:
            config.perf_est_list_path = get_norm_path(config.perf_est_list_path, prefix=lfs_files_dir_path)

        config.job_dir = dto.dir_path

        if config.iteration == 0:
            oracle_indexes, filenames = zero_iteration.run(config)
        else:
            oracle_indexes, perf_est_indexes, candidate_indexes, filenames, labels_pred = regular_iteration.run(config)
        

        log = "Job was successfully processed!"
        ended_at = get_current_utc_datetime()
        labellings = []

        if config.iteration == 0:
            labellings = []
            for i in oracle_indexes:
                labellings.append(LabellingInitializeSerializer(
                        job_id=job_id,
                        spectrum_filename=filenames[i],
                        spectrum_set=LabellingSpectrumSetType.ORACLE,
                        sequence_iteration=config.iteration,
                        model_prediction="-"
                ))
        else:
            indexes_set = [
                (oracle_indexes, LabellingSpectrumSetType.ORACLE),
                (perf_est_indexes, LabellingSpectrumSetType.PERFORMANCE_ESTIMATION)
            ]

            if config.show_candidates:
                indexes_set.append((candidate_indexes, LabellingSpectrumSetType.CANDIDATE))

            for indexes, spectrum_set in indexes_set:
                for i in indexes:
                    labellings.append(LabellingInitializeSerializer(
                        job_id=job_id,
                        spectrum_filename=filenames[i],
                        spectrum_set=spectrum_set,
                        sequence_iteration=config.iteration,
                        model_prediction=config.classes[labels_pred[i]]
                    ))
        labelling_api.initialize_labellings_batch(labellings)

        job_api.end_job_by_job_id_and_job_end_action(
            job_id, JobEndActionType.COMPLETE, JobEndSerializer(started_at=started_at, ended_at=ended_at)
        )
    except SystemExit:
        log = "Job was manually aborted!"

    except Exception:
        log = get_error_log()
        ended_at = get_current_utc_datetime()

        job_api.end_job_by_job_id_and_job_end_action(
            job_id, JobEndActionType.ERROR, JobEndSerializer(started_at=started_at, ended_at=ended_at)
        )

    finally:
        write_log_file(log_file_path, log)

