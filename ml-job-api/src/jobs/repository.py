from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from src.jobs.dto import (
    JobCreateDTO,
    JobUpdateDTO,
)
from src.jobs.entity import JobEntity


class JobRepository(ABC):
    """
    Repository interface for managing operations on job records.
    """

    @abstractmethod
    async def create(self, dto: JobCreateDTO) -> JobEntity:
        """
        Create a new job record in the system.

        Parameters:
            dto (JobCreateDTO): Data transfer object containing initial job parameters.

        Returns:
            JobEntity: The newly created job entity.
        """

        raise NotImplementedError

    @abstractmethod
    async def get_by_job_id(self, job_id: UUID) -> JobEntity:
        """
        Retrieve a job record by its unique identifier.

        Parameters:
            job_id (UUID): The UUID of the job to retrieve.

        Returns:
            JobEntity: The job entity matching the given `job_id`.
        """

        raise NotImplementedError

    @abstractmethod
    async def update_by_job_id(self, job_id: UUID, dto: JobUpdateDTO) -> JobEntity:
        """
        Update fields of an existing job record.

        Parameters:
            job_id (UUID): The UUID of the job to update.
            dto (JobUpdateDTO): Data transfer object containing fields to modify.

        Returns:
            JobEntity: The updated job entity reflecting the applied changes.
        """

        raise NotImplementedError

    @abstractmethod
    async def delete_by_job_id(self, job_id: UUID) -> None:
        """
        Delete a job record from the system.

        Parameters:
            job_id (UUID): The UUID of the job to delete.
        """

        raise NotImplementedError

    @abstractmethod
    async def list_by_offset_and_limit(self, offset: int, limit: int) -> list[JobEntity]:
        """
        List job records in descending creation order, with pagination.

        Parameters:
            offset (int): Number of records to skip before starting the list.
            limit (int): Maximum number of records to return.

        Returns:
            list[JobEntity]: A list of job entities ordered by `created_at` descending.
        """

        raise NotImplementedError

    @abstractmethod
    async def total(self) -> int:
        """
        Get the total count of job records in the system.

        Returns:
            int: The total number of jobs.
        """

        raise NotImplementedError
