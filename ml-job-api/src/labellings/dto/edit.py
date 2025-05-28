from pydantic import (
    BaseModel,
    Field,
)

from src.labellings.resources import labelling_resources


class LabellingEditDTO(BaseModel):
    """
    Data Transfer Object model for editing an existing labelling's user-provided fields.
    """

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
