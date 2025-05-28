from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import job_resources


class JobEndDTO(BaseModel):
    """
    Data Transfer Object model used by workers to report job completion or failure metrics.
    """

    started_at: datetime = Field(
        ...,
        description=job_resources["started_at"]["DESCRIPTION"],
        examples=job_resources["started_at"]["EXAMPLES"],
    )

    ended_at: datetime = Field(
        ...,
        description=job_resources["ended_at"]["DESCRIPTION"],
        examples=job_resources["ended_at"]["EXAMPLES"],
    )
