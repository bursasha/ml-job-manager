from uuid import UUID

from sqlalchemy import (
    case,
    insert,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.labellings.dto import (
    LabellingCreateDTO,
    LabellingUpdateDTO,
)
from src.labellings.entity import LabellingEntity
from src.labellings.errors import (
    LabellingAbsentJobError,
    LabellingNotExistError,
)
from src.labellings.models import LabellingPostgresModel
from src.labellings.repository import LabellingRepository
from src.labellings.types import SpectrumSetType


class LabellingPostgresRepository(LabellingRepository):
    """
    PostgreSQL-backed implementation of LabellingRepository using SQLAlchemy AsyncSession.
    """

    model = LabellingPostgresModel

    def __init__(self, postgres_async_session: AsyncSession) -> None:
        """
        Initialize the repository with an async SQLAlchemy session.

        Parameters:
            postgres_async_session (AsyncSession): An AsyncSession bound to the PostgreSQL engine.
        """

        self.session = postgres_async_session

    async def create(self, dto: LabellingCreateDTO) -> LabellingEntity:
        """
        Insert a new labelling record into the database.

        Parameters:
            dto (LabellingCreateDTO): DTO containing all fields for the new labelling.

        Returns:
            LabellingEntity: The created labelling entity.

        Raises:
            LabellingAbsentJobError: If the referenced job_id does not exist.
        """

        orm = self.model(**dto.model_dump(exclude_none=True))

        self.session.add(orm)

        try:
            await self.session.commit()

        except IntegrityError as e:
            await self.session.rollback()
            raise LabellingAbsentJobError(f"Cannot create labelling with associated job ID={dto.job_id}.") from e

        await self.session.refresh(orm)

        return LabellingEntity.model_validate(orm)

    async def create_batch(self, batch: list[LabellingCreateDTO]) -> None:
        """
        Bulk-insert multiple labelling records in one operation.

        Parameters:
            batch (list[LabellingCreateDTO]): List of DTOs containing all fields for the new labellings.

        Raises:
            LabellingAbsentJobError: If any DTO references a non-existent job_id.
        """

        # Prepare and execute bulk creation
        batch_creation_data = [dto.model_dump(exclude_none=True) for dto in batch]
        query = insert(self.model)

        try:
            await self.session.execute(query, batch_creation_data)
            await self.session.commit()

        except IntegrityError as e:
            await self.session.rollback()
            raise LabellingAbsentJobError("Cannot create some labelling of the batch.") from e

    async def get_by_labelling_id(self, labelling_id: UUID) -> LabellingEntity:
        """
        Fetch a labelling record by its UUID key.

        Parameters:
            labelling_id (UUID): The unique identifier of the labelling.

        Returns:
            LabellingEntity: The labelling entity matching the given ID.

        Raises:
            LabellingNotExistError: If no labelling with the specified ID exists.
        """

        orm = await self.session.get(self.model, labelling_id)

        if not orm:
            raise LabellingNotExistError(f"Cannot get labelling with ID={labelling_id}.")

        return LabellingEntity.model_validate(orm)

    async def update_by_labelling_id(self, labelling_id: UUID, dto: LabellingUpdateDTO) -> LabellingEntity:
        """
        Update user-given metadata for an existing labelling.

        Parameters:
            labelling_id (UUID): The unique identifier of the labelling to update.
            dto (LabellingUpdateDTO): DTO containing fields to modify.

        Returns:
            LabellingEntity: The updated labelling entity.

        Raises:
            LabellingNotExistError: If no labelling with the specified ID exists.
        """

        orm = await self.session.get(self.model, labelling_id)

        if not orm:
            raise LabellingNotExistError(f"Cannot update labelling with ID={labelling_id}.")

        for key, value in dto.model_dump(exclude_none=True).items():
            setattr(orm, key, value)

        await self.session.commit()
        await self.session.refresh(orm)

        return LabellingEntity.model_validate(orm)

    async def update_batch_by_labelling_ids(self, labelling_ids: list[UUID], batch: list[LabellingUpdateDTO]) -> None:
        """
        Apply bulk updates to multiple labelling records in one operation.

        Parameters:
            labelling_ids (list[UUID]): List of UUIDs identifying the labellings to update.
            batch (list[LabellingUpdateDTO]): Parallel list of DTOs with updated fields.

        Raises:
            LabellingNotExistError: If any labelling ID in the list does not exist.
        """

        # Verify all IDs exist
        query = select(self.model.labelling_id).where(self.model.labelling_id.in_(labelling_ids))
        result = await self.session.execute(query)
        existing_ids = result.scalars().all()

        if len(labelling_ids) != len(existing_ids):
            raise LabellingNotExistError("Cannot update some labelling of the batch.")

        # Prepare and execute bulk update
        batch_update_data = [
            dict(labelling_id=labelling_id, **dto.model_dump(exclude_none=True))
            for labelling_id, dto in zip(labelling_ids, batch)
        ]
        query = update(self.model)

        await self.session.execute(query, batch_update_data)
        await self.session.commit()

    async def list_by_job_id(self, job_id: UUID) -> list[LabellingEntity]:
        """
        Retrieve all labelling records for a given job, ordered by spectrum_set priority.

        Parameters:
            job_id (UUID): The UUID of the job whose labellings to list.

        Returns:
            list[LabellingEntity]: Labelling entities sorted by ORACLE → PERFORMANCE_ESTIMATION → CANDIDATE.
        """

        spectrum_set_order = case(
            (SpectrumSetType.ORACLE == self.model.spectrum_set, 1),
            (SpectrumSetType.PERFORMANCE_ESTIMATION == self.model.spectrum_set, 2),
            (SpectrumSetType.CANDIDATE == self.model.spectrum_set, 3),
            else_=4,
        )
        query = select(self.model).where(job_id == self.model.job_id).order_by(spectrum_set_order)
        result = await self.session.execute(query)
        orms = result.scalars().all()

        return [LabellingEntity.model_validate(orm) for orm in orms]
