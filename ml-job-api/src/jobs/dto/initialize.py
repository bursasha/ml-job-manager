from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import job_resources
from src.jobs.types import JobType


class JobInitializeDTO(BaseModel):
    """
    Data Transfer Object model for initializing a new Job.
    """

    type: JobType = Field(
        ...,
        description=job_resources["type"]["DESCRIPTION"],
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
