from src.files.repositories import FileLFSRepository
from src.files.service import FileService
from src.infrastructure.storages import lfs_files_dir_path


def get_service_using_lfs() -> FileService:
    """
    Construct a FileService backed by the local filesystem repository.

    This dependency factory builds a FileLFSRepository with the configured
    shared files directory path, and injects it into a FileService instance.

    Returns:
        FileService: Service instance for handling file and directory operations
                     using the local filesystem storage backend.
    """

    lfs_repository = FileLFSRepository(lfs_files_dir_path)

    return FileService(lfs_repository)
