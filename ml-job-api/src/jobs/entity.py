from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from src.jobs.resources import job_resources
from src.jobs.types import (
    JobType,
    PhaseType,
)


class JobEntity(BaseModel):
    """
    Entity model representing a background ML job metadata.
    """

    model_config = ConfigDict(from_attributes=True)

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
        PhaseType.PENDING,
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

    created_at: datetime | None = Field(
        None,
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
