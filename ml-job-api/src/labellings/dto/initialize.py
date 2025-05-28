from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from src.labellings.resources import labelling_resources
from src.labellings.types import SpectrumSetType


class LabellingInitializeDTO(BaseModel):
    """
    Data Transfer Object model for initializing a new labelling.
    """

    job_id: UUID = Field(
        ...,
        description=labelling_resources["job_id"]["DESCRIPTION"],
    )

    spectrum_filename: str = Field(
        ...,
        min_length=labelling_resources["spectrum_filename"]["MIN_LENGTH"],
        max_length=labelling_resources["spectrum_filename"]["MAX_LENGTH"],
        description=labelling_resources["spectrum_filename"]["DESCRIPTION"],
        examples=labelling_resources["spectrum_filename"]["EXAMPLES"],
    )

    spectrum_set: SpectrumSetType = Field(
        ...,
        description=labelling_resources["spectrum_set"]["DESCRIPTION"],
    )

    sequence_iteration: int = Field(
        ...,
        ge=labelling_resources["sequence_iteration"]["MIN_VALUE"],
        description=labelling_resources["sequence_iteration"]["DESCRIPTION"],
        examples=labelling_resources["sequence_iteration"]["EXAMPLES"],
    )

    model_prediction: str | None = Field(
        None,
        min_length=labelling_resources["model_prediction"]["MIN_LENGTH"],
        max_length=labelling_resources["model_prediction"]["MAX_LENGTH"],
        description=labelling_resources["model_prediction"]["DESCRIPTION"],
        examples=labelling_resources["model_prediction"]["EXAMPLES"],
    )

    user_label: str | None = Field(
        None,
        min_length=labelling_resources["user_label"]["MIN_LENGTH"],
        max_length=labelling_resources["user_label"]["MAX_LENGTH"],
        description=labelling_resources["user_label"]["DESCRIPTION"],
        examples=labelling_resources["user_label"]["EXAMPLES"],
    )

    user_comment: str | None = Field(
        None,
        min_length=labelling_resources["user_comment"]["MIN_LENGTH"],
        max_length=labelling_resources["user_comment"]["MAX_LENGTH"],
        description=labelling_resources["user_comment"]["DESCRIPTION"],
        examples=labelling_resources["user_comment"]["EXAMPLES"],
    )
