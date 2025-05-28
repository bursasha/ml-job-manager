from pydantic import (
    BaseModel,
    Field,
)

from src.files.resources import list_resources
from src.files.serializers.summarize import (
    DirectorySummarizeSerializer,
    FileSummarizeSerializer,
)


class EntryListSerializer(BaseModel):
    """
    Serializer model for listing the contents of a directory.
    """

    parent_dir_path: str = Field(
        ...,
        description=list_resources["parent_dir_path"]["DESCRIPTION"],
        examples=list_resources["parent_dir_path"]["EXAMPLES"],
    )

    total: int = Field(
        ...,
        description=list_resources["total"]["DESCRIPTION"],
        examples=list_resources["total"]["EXAMPLES"],
    )

    file_count: int = Field(
        ...,
        description=list_resources["file_count"]["DESCRIPTION"],
        examples=list_resources["file_count"]["EXAMPLES"],
    )

    directory_count: int = Field(
        ...,
        description=list_resources["directory_count"]["DESCRIPTION"],
        examples=list_resources["directory_count"]["EXAMPLES"],
    )

    files: list[FileSummarizeSerializer] = Field(
        ...,
        description=list_resources["files"]["DESCRIPTION"],
    )

    directories: list[DirectorySummarizeSerializer] = Field(
        ...,
        description=list_resources["directories"]["DESCRIPTION"],
    )
