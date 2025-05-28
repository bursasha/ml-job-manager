from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.clients import celery_client
from src.infrastructure.storages import get_postgres_async_session
from src.jobs.clients import JobCeleryQueue
from src.jobs.repositories import JobPostgresRepository
from src.jobs.service import JobService


def get_service_using_postgres_and_celery(
    postgres_async_session: AsyncSession = Depends(get_postgres_async_session),
) -> JobService:
    """
    Construct a JobService backed by PostgreSQL persistence and Celery task queue.

    This dependency factory builds a JobPostgresRepository using the injected
    AsyncSession, and a JobCeleryQueue using the global Celery client, then
    injects both into a JobService instance.

    Parameters:
        postgres_async_session (AsyncSession): Asynchronous database session for PostgreSQL operations.

    Returns:
        JobService: Service instance for managing job lifecycle and dispatching tasks to Celery for processing.
    """

    postgres_repository = JobPostgresRepository(postgres_async_session)
    celery_queue = JobCeleryQueue(celery_client)

    return JobService(postgres_repository, celery_queue)
