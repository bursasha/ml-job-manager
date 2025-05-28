from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import job_resources
from src.jobs.types import (
    JobType,
    PhaseType,
)


class JobSummarizeSerializer(BaseModel):
    """
    Serializer model of summary representation of a job record.
    """

    phase: PhaseType = Field(
        ...,
        description=job_resources["phase"]["DESCRIPTION"],
    )

    type: JobType = Field(
        ...,
        description=job_resources["type"]["DESCRIPTION"],
    )

    job_id: UUID = Field(
        ...,
        description=job_resources["job_id"]["DESCRIPTION"],
    )

    label: str = Field(
        ...,
        description=job_resources["label"]["DESCRIPTION"],
        examples=job_resources["label"]["EXAMPLES"],
    )

    created_at: datetime = Field(
        ...,
        description=job_resources["created_at"]["DESCRIPTION"],
        examples=job_resources["created_at"]["EXAMPLES"],
    )

    started_at: datetime | None = Field(
        None,
        description=job_resources["started_at"]["DESCRIPTION"],
        examples=job_resources["started_at"]["EXAMPLES"],
    )

    ended_at: datetime | None = Field(
        None,
        description=job_resources["ended_at"]["DESCRIPTION"],
        examples=job_resources["ended_at"]["EXAMPLES"],
    )

    execution_duration: float | None = Field(
        None,
        description=job_resources["execution_duration"]["DESCRIPTION"],
        examples=job_resources["execution_duration"]["EXAMPLES"],
    )
