from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.settings.storages import (
    lfs_settings,
    postgres_settings,
)


#


# Local filesystem storage paths, loaded from environment via LFSSettings
lfs_files_dir_path = lfs_settings.files_dir_path

# Local filesystem storage paths, loaded from environment via LFSSettings
lfs_spectra_dir_path = lfs_settings.spectra_dir_path


#


# Async PostgreSQL engine for all DB operations
postgres_async_engine = create_async_engine(
    url=postgres_settings.db_url,
    echo=postgres_settings.debug,
    connect_args={"timeout": postgres_settings.engine_connection_timeout},
    future=True,
)

# Async session maker configured with commit/flush/expire settings
postgres_async_session_maker = async_sessionmaker(
    bind=postgres_async_engine,
    autocommit=postgres_settings.session_autocommit,
    autoflush=postgres_settings.session_autoflush,
    expire_on_commit=postgres_settings.session_expire_on_commit,
    future=True,
)


async def get_postgres_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an asynchronous SQLAlchemy session.

    Use as a dependency to perform database operations within an async context.
    The session is closed automatically when the generator exits.

    Returns:
        AsyncSession: A SQLAlchemy async session bound to the engine.
    """

    async with postgres_async_session_maker() as postgres_async_session:
        yield postgres_async_session
