from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from src.jobs.dto import JobStartDTO
from src.jobs.types import JobType


class JobQueue(ABC):
    """
    Interface for managing asynchronous ML jobs.
    """

    @abstractmethod
    def run_by_job_id_and_job_type(self, job_id: UUID, job_type: JobType, dto: JobStartDTO) -> None:
        """
        Enqueue a new job for execution.

        Parameters:
            job_id (UUID): Unique identifier assigned to the job.
            job_type (JobType): The category of the job, determining which worker job to invoke.
            dto (JobStartDTO): Data transfer object containing initialization parameters for the job.
        """

        raise NotImplementedError

    @abstractmethod
    def abort_by_job_id(self, job_id: UUID) -> None:
        """
        Revoke a running job.

        Parameters:
            job_id (UUID): Unique identifier of the job to abort.
        """

        raise NotImplementedError
