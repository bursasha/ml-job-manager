from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.jobs.dto import (
    JobCreateDTO,
    JobUpdateDTO,
)
from src.jobs.entity import JobEntity
from src.jobs.errors import JobNotExistError
from src.jobs.models import JobPostgresModel
from src.jobs.repository import JobRepository


class JobPostgresRepository(JobRepository):
    """
    PostgreSQL-backed implementation of JobRepository using SQLAlchemy AsyncSession.
    """

    model = JobPostgresModel

    def __init__(self, postgres_async_session: AsyncSession) -> None:
        """
        Initialize the repository with an async SQLAlchemy session.

        Parameters:
            postgres_async_session (AsyncSession): An SQLAlchemy AsyncSession bound to the PostgreSQL engine.
        """

        self.session = postgres_async_session

    async def create(self, dto: JobCreateDTO) -> JobEntity:
        """
        Insert a new job record into the database.

        Parameters:
            dto (JobCreateDTO): DTO containing initial job fields.

        Returns:
            JobEntity: The created job entity.
        """

        orm = self.model(**dto.model_dump(exclude_none=True))

        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)

        return JobEntity.model_validate(orm)

    async def get_by_job_id(self, job_id: UUID) -> JobEntity:
        """
        Fetch a job record by its UUID key.

        Parameters:
            job_id (UUID): The unique identifier of the job.

        Returns:
            JobEntity: The job entity matching the given ID.

        Raises:
            JobNotExistError: If no job with the specified ID exists.
        """

        orm = await self.session.get(self.model, job_id)

        if not orm:
            raise JobNotExistError(f"Cannot get job with ID={job_id}.")

        return JobEntity.model_validate(orm)

    async def update_by_job_id(self, job_id: UUID, dto: JobUpdateDTO) -> JobEntity:
        """
        Update existing fields of a job record.

        Parameters:
            job_id (UUID): The unique identifier of the job to update.
            dto (JobUpdateDTO): DTO containing fields to update.

        Returns:
            JobEntity: The updated job entity reflecting persisted changes.

        Raises:
            JobNotExistError: If no job with the specified ID exists.
        """

        orm = await self.session.get(self.model, job_id)

        if not orm:
            raise JobNotExistError(f"Cannot update job with ID={job_id}.")

        for key, value in dto.model_dump(exclude_none=True).items():
            setattr(orm, key, value)

        await self.session.commit()
        await self.session.refresh(orm)

        return JobEntity.model_validate(orm)

    async def delete_by_job_id(self, job_id: UUID) -> None:
        """
        Delete a job record from the database.

        Parameters:
            job_id (UUID): The unique identifier of the job to delete.

        Raises:
            JobNotExistError: If no job with the specified ID exists.
        """

        orm = await self.session.get(self.model, job_id)

        if not orm:
            raise JobNotExistError(f"Cannot delete job with ID={job_id}.")

        await self.session.delete(orm)
        await self.session.commit()

    async def list_by_offset_and_limit(self, offset: int, limit: int) -> list[JobEntity]:
        """
        Retrieve a page of job records ordered by creation time descending.

        Parameters:
            offset (int): Number of records to skip.
            limit (int): Maximum number of records to return.

        Returns:
            list[JobEntity]: A list of job entities for the requested page.
        """

        created_at_order = self.model.created_at.desc()
        query = select(self.model).order_by(created_at_order).offset(offset).limit(limit)
        result = await self.session.execute(query)
        orms = result.scalars().all()

        return [JobEntity.model_validate(orm) for orm in orms]

    async def total(self) -> int:
        """
        Count the total number of job records.

        Returns:
            int: Total count of jobs in the database.
        """

        query = select(func.count(self.model.job_id))
        result = await self.session.execute(query)
        total = result.scalar()

        if not total:
            return 0

        return total
