from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from src.labellings.dto import (
    LabellingCreateDTO,
    LabellingUpdateDTO,
)
from src.labellings.entity import LabellingEntity


class LabellingRepository(ABC):
    """
    Repository interface for managing spectrum labelling records associated with Active ML jobs.
    """

    @abstractmethod
    async def create(self, dto: LabellingCreateDTO) -> LabellingEntity:
        """
        Create and persist a new labelling record.

        Parameters:
            dto (LabellingCreateDTO): Data transfer object for job creation.

        Returns:
            LabellingEntity: The newly created labelling entity.
        """

        raise NotImplementedError

    @abstractmethod
    async def create_batch(self, batch: list[LabellingCreateDTO]) -> None:
        """
        Create multiple labelling records in a single bulk operation.

        Parameters:
            batch (list[LabellingCreateDTO]): List of DTOs for each labelling to initialize.
        """

        raise NotImplementedError

    @abstractmethod
    async def get_by_labelling_id(self, labelling_id: UUID) -> LabellingEntity:
        """
        Retrieve a labelling record by its unique identifier.

        Parameters:
            labelling_id (UUID): The UUID of the labelling to retrieve.

        Returns:
            LabellingEntity: The labelling entity matching the given ID.
        """

        raise NotImplementedError

    @abstractmethod
    async def update_by_labelling_id(self, labelling_id: UUID, dto: LabellingUpdateDTO) -> LabellingEntity:
        """
        Update user-provided metadata for an existing labelling.

        Parameters:
            labelling_id (UUID): The UUID of the labelling to update.
            dto (LabellingUpdateDTO): DTO containing new labelling metadata.

        Returns:
            LabellingEntity: The updated labelling entity reflecting applied changes.
        """

        raise NotImplementedError

    @abstractmethod
    async def update_batch_by_labelling_ids(self, labelling_ids: list[UUID], batch: list[LabellingUpdateDTO]) -> None:
        """
        Apply bulk updates to multiple labelling records in one operation.

        Parameters:
            labelling_ids (list[UUID]): List of labelling UUIDs to update.
            batch (list[LabellingUpdateDTO]): Parallel list of DTOs with updated metadata for each corresponding ID.
        """

        raise NotImplementedError

    @abstractmethod
    async def list_by_job_id(self, job_id: UUID) -> list[LabellingEntity]:
        """
        List all labelling records associated with a given job.

        Parameters:
            job_id (UUID): The UUID of the job whose labellings to retrieve.

        Returns:
            list[LabellingEntity]: A list of all labelling entities tied to the job.
        """

        raise NotImplementedError
