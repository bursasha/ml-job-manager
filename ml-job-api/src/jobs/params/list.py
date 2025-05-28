from pydantic import (
    BaseModel,
    Field,
)

from src.jobs.resources import list_resources


class JobListParams(BaseModel):
    """
    Query parameters for paginating job listings.
    """

    offset: int = Field(
        list_resources["offset"]["DEFAULT_VALUE"],
        ge=list_resources["offset"]["MIN_VALUE"],
        description=list_resources["offset"]["DESCRIPTION"],
        examples=list_resources["offset"]["EXAMPLES"],
    )

    limit: int = Field(
        list_resources["limit"]["DEFAULT_VALUE"],
        ge=list_resources["limit"]["MIN_VALUE"],
        description=list_resources["limit"]["DESCRIPTION"],
        examples=list_resources["limit"]["EXAMPLES"],
    )
