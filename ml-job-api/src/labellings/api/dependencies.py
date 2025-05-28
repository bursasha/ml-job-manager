from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.storages import get_postgres_async_session
from src.labellings.repositories import LabellingPostgresRepository
from src.labellings.service import LabellingService


def get_service_using_postgres(
    postgres_async_session: AsyncSession = Depends(get_postgres_async_session),
) -> LabellingService:
    """
    Construct a LabellingService backed by PostgreSQL persistence.

    This dependency factory builds a LabellingPostgresRepository using the injected
    AsyncSession, and injects it into a LabellingService instance.

    Parameters:
        postgres_async_session (AsyncSession): Asynchronous database session for PostgreSQL operations.

    Returns:
        LabellingService: Service instance for labelling records using the PostgreSQL backend.
    """

    postgres_repository = LabellingPostgresRepository(postgres_async_session)

    return LabellingService(postgres_repository)
