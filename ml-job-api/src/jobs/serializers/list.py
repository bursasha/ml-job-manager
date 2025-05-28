from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import list_resources
from src.jobs.serializers.summarize import JobSummarizeSerializer


class JobListSerializer(BaseModel):
    """
    Serializer model for paginated listing of jobs.
    """

    total: int = Field(
        ...,
        description=list_resources["total"]["DESCRIPTION"],
        examples=list_resources["total"]["EXAMPLES"],
    )

    offset: int = Field(
        ...,
        description=list_resources["offset"]["DESCRIPTION"],
        examples=list_resources["offset"]["EXAMPLES"],
    )

    limit: int = Field(
        ...,
        description=list_resources["limit"]["DESCRIPTION"],
        examples=list_resources["limit"]["EXAMPLES"],
    )

    jobs: list[JobSummarizeSerializer] = Field(
        ...,
        description=list_resources["jobs"]["DESCRIPTION"],
    )
