from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from src.labellings.resources import list_resources
from src.labellings.serializers.read import LabellingReadSerializer


class LabellingListSerializer(BaseModel):
    """
    Serializer model for returning a paginated list of labellings associated with a specific job.
    """

    job_id: UUID = Field(
        ...,
        description=list_resources["job_id"]["DESCRIPTION"],
    )

    total: int = Field(
        ...,
        description=list_resources["total"]["DESCRIPTION"],
        examples=list_resources["total"]["EXAMPLES"],
    )

    labellings: list[LabellingReadSerializer] = Field(
        ...,
        description=list_resources["labellings"]["DESCRIPTION"],
    )
