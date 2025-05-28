from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)

from src.files.resources import (
    directory_resources,
    file_resources,
)


class FileReadSerializer(BaseModel):
    """
    Serializer model for file metadata.
    """

    filename: str = Field(
        ...,
        description=file_resources["filename"]["DESCRIPTION"],
        examples=file_resources["filename"]["EXAMPLES"],
    )

    parent_dir_path: str = Field(
        ...,
        description=file_resources["parent_dir_path"]["DESCRIPTION"],
        examples=file_resources["parent_dir_path"]["EXAMPLES"],
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


class DirectoryReadSerializer(BaseModel):
    """
    Serializer model for directory metadata.
    """

    dirname: str = Field(
        ...,
        description=directory_resources["dirname"]["DESCRIPTION"],
        examples=directory_resources["dirname"]["EXAMPLES"],
    )

    parent_dir_path: str = Field(
        ...,
        description=directory_resources["parent_dir_path"]["DESCRIPTION"],
        examples=directory_resources["parent_dir_path"]["EXAMPLES"],
    )
