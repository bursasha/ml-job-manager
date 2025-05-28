from pydantic import (
    BaseModel,
    Field,
)

from src.files.resources import file_resources


class EntryLocateParams(BaseModel):
    """
    Query parameters for locating a file or directory within storage.
    """

    parent_dir_path: str = Field(
        ...,
        min_length=file_resources["parent_dir_path"]["MIN_LENGTH"],
        pattern=file_resources["parent_dir_path"]["PATTERN"],
        description=file_resources["parent_dir_path"]["DESCRIPTION"],
        examples=file_resources["parent_dir_path"]["EXAMPLES"],
    )
