from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)


class JobEndSerializer(BaseModel):
    """
    Serializer model used by workers to report job completion or failure metrics.
    """

    started_at: datetime = Field(
        ...,
        description="UTC datetime when job execution started",
        examples=["2025-03-21T12:40:00Z"],
    )

    ended_at: datetime = Field(
        ...,
        description="UTC datetime when job execution ended",
        examples=["2025-03-21T12:45:00Z"],
    )
