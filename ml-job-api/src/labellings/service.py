from uuid import UUID

from src.common.utils import generate_uuid
from src.labellings.dto import (
    LabellingCreateDTO,
    LabellingEditDTO,
    LabellingInitializeDTO,
    LabellingUpdateDTO,
)
from src.labellings.errors import LabellingInvalidBatchError
from src.labellings.repository import LabellingRepository
from src.labellings.serializers import (
    LabellingListSerializer,
    LabellingReadSerializer,
)


class LabellingService:
    """
    Business logic layer for managing labelling operations on spectra for Active ML Job.
    """

    def __init__(self, repository: LabellingRepository) -> None:
        """
        Initialize the labelling service with a repository implementation.

        Parameters:
            repository (LabellingRepository): Concrete repository for persisting and retrieving labelling entities.
        """

        self.repository = repository

    @staticmethod
    def _generate_labelling_id() -> UUID:
        """
        Generate a new UUID for a labelling record.

        Returns:
            UUID: A newly generated labelling identifier.
        """

        labelling_id = generate_uuid()

        return labelling_id

    async def initialize_labelling(self, dto: LabellingInitializeDTO) -> LabellingReadSerializer:
        """
        Create and persist a single new labelling record.

        Parameters:
            dto (LabellingInitializeDTO): DTO for job creation.

        Returns:
            LabellingReadSerializer: Serializer with the full details of the newly created labelling.
        """

        labelling_id = self._generate_labelling_id()
        entity = await self.repository.create(LabellingCreateDTO(labelling_id=labelling_id, **dto.model_dump()))

        return LabellingReadSerializer(**entity.model_dump())

    async def initialize_labellings_batch(self, batch: list[LabellingInitializeDTO]) -> None:
        """
        Bulk create and persist multiple labelling records in one operation.

        Parameters:
            batch (list[LabellingInitializeDTO]): List of DTOs for each new labelling.
        """

        labelling_ids = [self._generate_labelling_id() for _ in batch]
        batch = [
            LabellingCreateDTO(labelling_id=labelling_id, **dto.model_dump())
            for labelling_id, dto in zip(labelling_ids, batch)
        ]

        await self.repository.create_batch(batch)

    async def retrieve_labelling_by_labelling_id(self, labelling_id: UUID) -> LabellingReadSerializer:
        """
        Retrieve a single labelling record by its unique identifier.

        Parameters:
            labelling_id (UUID): The UUID of the labelling to fetch.

        Returns:
            LabellingReadSerializer: Serializer containing the retrieved labelling’s details.
        """

        entity = await self.repository.get_by_labelling_id(labelling_id)

        return LabellingReadSerializer(**entity.model_dump())

    async def edit_labelling_by_labelling_id(
        self, labelling_id: UUID, dto: LabellingEditDTO
    ) -> LabellingReadSerializer:
        """
        Apply user edits to an existing labelling record.

        Parameters:
            labelling_id (UUID): The UUID of the labelling to update.
            dto (LabellingEditDTO): DTO containing the new metadata.

        Returns:
            LabellingReadSerializer: Serializer with the updated labelling details.
        """

        entity = await self.repository.update_by_labelling_id(labelling_id, LabellingUpdateDTO(**dto.model_dump()))

        return LabellingReadSerializer(**entity.model_dump())

    async def edit_labellings_batch_by_labelling_ids(
        self, labelling_ids: list[UUID], batch: list[LabellingEditDTO]
    ) -> None:
        """
        Apply user edits to multiple existing labellings in a bulk operation.

        Parameters:
            labelling_ids (list[UUID]): List of labelling UUIDs to update.
            batch (list[LabellingEditDTO]): Parallel list of DTOs containing edits.

        Raises:
            LabellingInvalidBatchError: If the lengths of `labelling_ids` and `batch` differ.
        """

        if len(labelling_ids) != len(batch):
            raise LabellingInvalidBatchError("Cannot edit labellings batch with inappropriate IDs for the batch.")

        batch = [LabellingUpdateDTO(**dto.model_dump()) for dto in batch]

        await self.repository.update_batch_by_labelling_ids(labelling_ids, batch)

    async def list_labellings_by_job_id(self, job_id: UUID) -> LabellingListSerializer:
        """
        List all labelling records associated with a given job.

        Parameters:
            job_id (UUID): The UUID of the job whose labellings are requested.

        Returns:
            LabellingListSerializer: Serializer with the total count and list of LabellingReadSerializer for the job.
        """

        entities = await self.repository.list_by_job_id(job_id)
        serializers = [LabellingReadSerializer(**entity.model_dump()) for entity in entities]
        total = len(serializers)

        return LabellingListSerializer(job_id=job_id, total=total, labellings=serializers)
