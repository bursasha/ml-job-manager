from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)

from src.files.resources import (
    directory_resources,
    file_resources,
)


class FileSummarizeSerializer(BaseModel):
    """
    Serializer model for summary view for a file metadata.
    """

    filename: str = Field(
        ...,
        description=file_resources["filename"]["DESCRIPTION"],
        examples=file_resources["filename"]["EXAMPLES"],
    )

    size: int = Field(
        ...,
        description=file_resources["size"]["DESCRIPTION"],
        examples=file_resources["size"]["EXAMPLES"],
    )

    modified_at: datetime = Field(
        ...,
        description=file_resources["modified_at"]["DESCRIPTION"],
        examples=file_resources["modified_at"]["EXAMPLES"],
    )


class DirectorySummarizeSerializer(BaseModel):
    """
    Serializer model for summary view for a directory metadata.
    """

    dirname: str = Field(
        ...,
        description=directory_resources["dirname"]["DESCRIPTION"],
        examples=directory_resources["dirname"]["EXAMPLES"],
    )
