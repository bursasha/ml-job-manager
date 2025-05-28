from pydantic import (
    AmqpDsn,
    Field,
    field_validator,
)
from pydantic_settings import BaseSettings


class CelerySettings(BaseSettings):
    """
    Configuration settings for the Celery job publishing and revoking.
    All values can be loaded from environment variables.
    """

    broker_url: str = Field(
        ...,
        description="AMQP broker DSN used by Celery to send and receive job messages",
    )

    task_default_queue: str = Field(
        ...,
        description="Name of the default queue to which jobs are published",
    )

    task_publish_retry: bool = Field(
        True,
        description="Whether to automatically retry publishing jobs on broker failure",
    )

    @field_validator("broker_url")
    def build_broker_url(cls, broker_url: str) -> str:
        broker_dsn = AmqpDsn(broker_url)

        return str(broker_dsn)


celery_settings = CelerySettings()
