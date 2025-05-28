from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import job_resources


class JobStartDTO(BaseModel):
    """
    Data Transfer Object model used to initiate the asynchronous execution of a Job.
    """

    dir_path: str = Field(
        ...,
        min_length=job_resources["dir_path"]["MIN_LENGTH"],
        max_length=job_resources["dir_path"]["MAX_LENGTH"],
        pattern=job_resources["dir_path"]["PATTERN"],
        description=job_resources["dir_path"]["DESCRIPTION"],
        examples=job_resources["dir_path"]["EXAMPLES"],
    )
