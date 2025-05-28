from pydantic import (
    Field,
    PostgresDsn,
    field_validator,
)
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    """
    Configuration settings for connecting to a PostgreSQL database asynchronously.
    All values can be loaded from environment variables.
    """

    db_url: str = Field(
        ...,
        description="Base PostgreSQL DSN used to build the connection URL",
    )

    debug: bool = Field(
        ...,
        description="Enable DB echo mode for detailed SQL logging",
    )

    engine_connection_timeout: int = Field(
        ...,
        description="Maximum seconds to wait when establishing a new DB connection",
    )

    session_autocommit: bool = Field(
        False,
        description="Automatically commit the transaction after each flush",
    )

    session_autoflush: bool = Field(
        False,
        description="Automatically flush pending changes to the database before query execution",
    )

    session_expire_on_commit: bool = Field(
        False,
        description="Expire ORM object state after commit, requiring reload on next access",
    )

    @field_validator("db_url")
    def build_db_async_url(cls, db_url: str) -> str:
        db_dsn = PostgresDsn(db_url)
        db_async_dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            hosts=db_dsn.hosts(),
            path=db_dsn.path.replace("/", ""),
            query=db_dsn.query,
            fragment=db_dsn.fragment,
        )

        return str(db_async_dsn)


postgres_settings = PostgresSettings()
