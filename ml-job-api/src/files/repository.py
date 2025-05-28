from abc import (
    ABC,
    abstractmethod,
)
from typing import AsyncIterator

from fastapi import UploadFile

from src.files.entities import (
    DirectoryEntity,
    FileEntity,
)


class FileRepository(ABC):
    """
    Repository interface for managing files and directories in the system storage.
    """

    @abstractmethod
    async def upload_by_filename_and_parent_dir_path(
        self, filename: str, parent_dir_path: str, file: UploadFile
    ) -> FileEntity:
        """
        Store an uploaded file in the given directory.

        Parameters:
            filename (str): The desired name under which to store the file.
            parent_dir_path (str): The target directory path (relative) where the file should be saved.
            file (UploadFile): The file object received via FastAPI's multipart upload.

        Returns:
            FileEntity: Entity model containing metadata about the newly stored file.
        """

        raise NotImplementedError

    @abstractmethod
    async def download_by_filename_and_parent_dir_path(
        self, filename: str, parent_dir_path: str
    ) -> AsyncIterator[bytes]:
        """
        Stream the contents of a stored file back to the caller.

        Parameters:
            filename (str): Name of the file to retrieve.
            parent_dir_path (str): Directory path where the file is stored.

        Returns:
            AsyncIterator[bytes]: An asynchronous iterator yielding chunks of the file's bytes.
        """

        raise NotImplementedError

    @abstractmethod
    async def delete_by_filename_and_parent_dir_path(self, filename: str, parent_dir_path: str) -> None:
        """
        Remove a file from the storage.

        Parameters:
            filename (str): Name of the file to delete.
            parent_dir_path (str): Directory path where the file resides.
        """

        raise NotImplementedError

    @abstractmethod
    async def create_by_dirname_and_parent_dir_path(self, dirname: str, parent_dir_path: str) -> DirectoryEntity:
        """
        Create a new directory in the storage.

        Parameters:
            dirname (str): Name of the directory to create.
            parent_dir_path (str): Parent directory path under which to create the new directory.

        Returns:
            DirectoryEntity: Entity model representing the created directory.
        """

        raise NotImplementedError

    @abstractmethod
    async def delete_by_dirname_and_parent_dir_path(self, dirname: str, parent_dir_path: str) -> None:
        """
        Remove a directory and its contents from the storage.

        Parameters:
            dirname (str): Name of the directory to delete.
            parent_dir_path (str): Parent directory path where the directory resides.
        """

        raise NotImplementedError

    @abstractmethod
    async def list_by_parent_dir_path(self, parent_dir_path: str) -> tuple[list[FileEntity], list[DirectoryEntity]]:
        """
        List all files and subdirectories under the given directory.

        Parameters:
            parent_dir_path (str): Directory path whose contents should be listed.

        Returns:
            Tuple[List[FileEntity], List[DirectoryEntity]]:
                Two lists: the first containing FileEntity items for each file,
                the second containing DirectoryEntity items for each subdirectory.
        """

        raise NotImplementedError
