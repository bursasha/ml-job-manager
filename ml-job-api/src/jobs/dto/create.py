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


class JobCreateDTO(BaseModel):
    """
    Data Transfer Object model for creating a new Job record.
    """

    job_id: UUID = Field(
        ...,
        description=job_resources["job_id"]["DESCRIPTION"],
    )

    dir_path: str = Field(
        ...,
        min_length=job_resources["dir_path"]["MIN_LENGTH"],
        max_length=job_resources["dir_path"]["MAX_LENGTH"],
        pattern=job_resources["dir_path"]["PATTERN"],
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
        min_length=job_resources["label"]["MIN_LENGTH"],
        max_length=job_resources["label"]["MAX_LENGTH"],
        description=job_resources["label"]["DESCRIPTION"],
        examples=job_resources["label"]["EXAMPLES"],
    )

    description: str | None = Field(
        None,
        min_length=job_resources["description"]["MIN_LENGTH"],
        max_length=job_resources["description"]["MAX_LENGTH"],
        description=job_resources["description"]["DESCRIPTION"],
        examples=job_resources["description"]["EXAMPLES"],
    )

    created_at: datetime = Field(
        ...,
        description=job_resources["created_at"]["DESCRIPTION"],
        examples=job_resources["created_at"]["EXAMPLES"],
    )
