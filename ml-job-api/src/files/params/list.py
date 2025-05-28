from pydantic import (
    BaseModel,
    Field,
)

from src.files.resources import list_resources


class EntryListParams(BaseModel):
    """
    Query parameters for listing directory contents.
    """

    parent_dir_path: str = Field(
        list_resources["parent_dir_path"]["DEFAULT_VALUE"],
        min_length=list_resources["parent_dir_path"]["MIN_LENGTH"],
        pattern=list_resources["parent_dir_path"]["PATTERN"],
        description=list_resources["parent_dir_path"]["DESCRIPTION"],
        examples=list_resources["parent_dir_path"]["EXAMPLES"],
    )
