from pydantic import (
    DirectoryPath,
    Field,
    field_validator,
)
from pydantic_settings import BaseSettings


class LFSSettings(BaseSettings):
    """
    Configuration settings for local filesystem storage.
    All values may be loaded from environment variables.
    """

    files_dir_path: str = Field(
        ...,
        description="Absolute path to the shared local filesystem directory used for storing files-related data",
    )

    spectra_dir_path: str = Field(
        ...,
        description="Absolute path to the shared local filesystem directory used for storing spectra-related data",
    )

    @field_validator("files_dir_path", "spectra_dir_path")
    def build_shared_dir_path(cls, shared_dir_path: str) -> str:
        dir_path = DirectoryPath(shared_dir_path)

        return str(dir_path)


lfs_settings = LFSSettings()
