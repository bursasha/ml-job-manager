from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import job_resources


class JobEditDTO(BaseModel):
    """
    Data Transfer Object model for editing an existing Job’s mutable fields.
    """

    description: str = Field(
        ...,
        min_length=job_resources["description"]["MIN_LENGTH"],
        max_length=job_resources["description"]["MAX_LENGTH"],
        description=job_resources["description"]["DESCRIPTION"],
        examples=job_resources["description"]["EXAMPLES"],
    )
