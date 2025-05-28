from pydantic import (
    AmqpDsn,
    Field,
    field_validator,
)
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    Configuration settings for the Celery-based worker application.
    All values may be loaded from environment variables.
    """

    broker_url: str = Field(
        ...,
        description="AMQP broker DSN for connecting the worker to the message broker",
    )

    broker_connection_timeout: int = Field(
        ...,
        description="Maximum seconds to wait when establishing a connection to the broker",
    )

    task_default_queue: str = Field(
        ...,
        description="Name of the queue from which the worker will consume jobs by default",
    )

    task_acks_late: bool = Field(
        True,
        description="If true, acknowledge jobs only after execution to avoid message loss",
    )

    task_track_started: bool = Field(
        True,
        description="Send a ‘task-started’ event when a job begins execution",
    )

    task_reject_on_worker_lost: bool = Field(
        True,
        description="Automatically reject and requeue jobs if the worker crashes mid‑execution",
    )

    broker_connection_retry_on_startup: bool = Field(
        True,
        description="Retry connecting to the broker on application startup if initial attempt fails",
    )

    broker_connection_max_retries: int | None = Field(
        None,
        description="Maximum number of broker connection retry attempts on startup (unlimited if None)",
    )

    worker_prefetch_multiplier: int = Field(
        1,
        description="Number of jobs to reserve at a time from the broker before acknowledging",
    )

    worker_send_task_events: bool = Field(
        True,
        description="Enable emission of job-related events for monitoring and inspection",
    )

    @field_validator("broker_url")
    def build_broker_url(cls, broker_url: str) -> str:
        broker_dsn = AmqpDsn(broker_url)

        return str(broker_dsn)


app_settings = AppSettings()
