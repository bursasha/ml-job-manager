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


class JobReadSerializer(BaseModel):
    """
    Serializer model of detailed representation of a single job record.
    """

    job_id: UUID = Field(
        ...,
        description=job_resources["job_id"]["DESCRIPTION"],
    )

    dir_path: str = Field(
        ...,
        description=job_resources["dir_path"]["DESCRIPTION"],
        examples=job_resources["dir_path"]["EXAMPLES"],
    )

    type: JobType = Field(
        ...,
        description=job_resources["type"]["DESCRIPTION"],
    )

    phase: PhaseType = Field(
        ...,
        description=job_resources["phase"]["DESCRIPTION"],
    )

    label: str = Field(
        ...,
        description=job_resources["label"]["DESCRIPTION"],
        examples=job_resources["label"]["EXAMPLES"],
    )

    description: str | None = Field(
        None,
        description=job_resources["description"]["DESCRIPTION"],
        examples=job_resources["description"]["EXAMPLES"],
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
