from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from src.labellings.resources import labelling_resources
from src.labellings.types import SpectrumSetType


class LabellingReadSerializer(BaseModel):
    """
    Serializer model for returning the complete details of a single labelling entry.
    """

    labelling_id: UUID = Field(
        ...,
        description=labelling_resources["labelling_id"]["DESCRIPTION"],
    )

    job_id: UUID = Field(
        ...,
        description=labelling_resources["job_id"]["DESCRIPTION"],
    )

    spectrum_filename: str = Field(
        ...,
        description=labelling_resources["spectrum_filename"]["DESCRIPTION"],
        examples=labelling_resources["spectrum_filename"]["EXAMPLES"],
    )

    spectrum_set: SpectrumSetType = Field(
        ...,
        description=labelling_resources["spectrum_set"]["DESCRIPTION"],
    )

    sequence_iteration: int = Field(
        ...,
        description=labelling_resources["sequence_iteration"]["DESCRIPTION"],
        examples=labelling_resources["sequence_iteration"]["EXAMPLES"],
    )

    model_prediction: str | None = Field(
        None,
        description=labelling_resources["model_prediction"]["DESCRIPTION"],
        examples=labelling_resources["model_prediction"]["EXAMPLES"],
    )

    user_label: str | None = Field(
        None,
        description=labelling_resources["user_label"]["DESCRIPTION"],
        examples=labelling_resources["user_label"]["EXAMPLES"],
    )

    user_comment: str | None = Field(
        None,
        description=labelling_resources["user_comment"]["DESCRIPTION"],
        examples=labelling_resources["user_comment"]["EXAMPLES"],
    )
