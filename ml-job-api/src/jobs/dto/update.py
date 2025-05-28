from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import job_resources
from src.jobs.types import PhaseType


class JobUpdateDTO(BaseModel):
    """
    Data Transfer Object model for updating various fields of an existing Job record.
    """

    description: str | None = Field(
        None,
        min_length=job_resources["description"]["MIN_LENGTH"],
        max_length=job_resources["description"]["MAX_LENGTH"],
        description=job_resources["description"]["DESCRIPTION"],
        examples=job_resources["description"]["EXAMPLES"],
    )

    phase: PhaseType | None = Field(
        None,
        description=job_resources["phase"]["DESCRIPTION"],
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
        ge=job_resources["execution_duration"]["MIN_VALUE"],
        description=job_resources["execution_duration"]["DESCRIPTION"],
        examples=job_resources["execution_duration"]["EXAMPLES"],
    )
