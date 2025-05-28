import os
from typing import AsyncIterator

import aiofiles
import aiofiles.os
import aioshutil
from fastapi import UploadFile

from src.common.utils import (
    get_datetime_from_timestamp,
    get_norm_path,
)
from src.files.entities import (
    DirectoryEntity,
    FileEntity,
)
from src.files.errors import (
    DirectoryAlreadyExistError,
    DirectoryNotExistError,
    FileNotExistError,
)
from src.files.repository import FileRepository
from src.files.utils import (
    download_file,
    upload_file,
)


class FileLFSRepository(FileRepository):
    """
    Local filesystem implementation of FileRepository.
    """

    chunk_size = 1024 * 1024

    def __init__(self, lfs_files_dir_path: str) -> None:
        """
        Initialize with the base directory path for file storage.

        Parameters:
            lfs_files_dir_path (str): Absolute path to the root of the shared files directory.
        """

        self.shared_dir_path = lfs_files_dir_path

    async def upload_by_filename_and_parent_dir_path(
        self, filename: str, parent_dir_path: str, file: UploadFile
    ) -> FileEntity:
        """
        Save an uploaded file under the specified directory.

        Parameters:
            filename (str): Desired name under which to store the file.
            parent_dir_path (str): Relative directory path where the file should be saved.
            file (UploadFile): The file object from FastAPI multipart upload.

        Returns:
            FileEntity: Metadata for the stored file, including size and modified timestamp.
        """

        # Build relative and absolute paths
        rel_parent_dir_path = get_norm_path(parent_dir_path)
        abs_parent_dir_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path)
        abs_file_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path, child_name=filename)

        # Ensure directory exists
        await aiofiles.os.makedirs(abs_parent_dir_path, exist_ok=True)

        # Write file in chunks
        await upload_file(abs_file_path, file, self.chunk_size)

        return FileEntity(
            filename=filename,
            parent_dir_path=rel_parent_dir_path,
            size=os.path.getsize(abs_file_path),
            modified_at=get_datetime_from_timestamp(os.path.getmtime(abs_file_path)),
        )

    async def download_by_filename_and_parent_dir_path(
        self, filename: str, parent_dir_path: str
    ) -> AsyncIterator[bytes]:
        """
        Stream a file's contents back to the caller.

        Parameters:
            filename (str): Name of the file to retrieve.
            parent_dir_path (str): Relative directory path where the file resides.

        Returns:
            AsyncIterator[bytes]: An async iterator yielding chunks of the file.

        Raises:
            FileNotExistError: If the file does not exist or is not a regular file.
        """

        # Build relative and absolute paths
        rel_file_path = get_norm_path(parent_dir_path, child_name=filename)
        abs_file_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path, child_name=filename)

        # Ensure file exists
        if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
            raise FileNotExistError(f"Cannot download file='{rel_file_path}'.")

        return download_file(abs_file_path, self.chunk_size)

    async def delete_by_filename_and_parent_dir_path(self, filename: str, parent_dir_path: str) -> None:
        """
        Delete a file from storage.

        Parameters:
            filename (str): Name of the file to delete.
            parent_dir_path (str): Relative directory path where the file resides.

        Raises:
            FileNotExistError: If the file does not exist or is not a regular file.
        """

        # Build relative and absolute paths
        rel_file_path = get_norm_path(parent_dir_path, child_name=filename)
        abs_file_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path, child_name=filename)

        # Ensure file exists
        if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
            raise FileNotExistError(f"Cannot delete file='{rel_file_path}'.")

        await aiofiles.os.remove(abs_file_path)

    async def create_by_dirname_and_parent_dir_path(self, dirname: str, parent_dir_path: str) -> DirectoryEntity:
        """
        Create a new directory under the specified parent path.

        Parameters:
            dirname (str): Name of the directory to create.
            parent_dir_path (str): Relative parent directory path.

        Returns:
            DirectoryEntity: Entity model for the created directory.

        Raises:
            DirectoryAlreadyExistError: If a directory with the same name already exists.
        """

        # Build relative and absolute paths
        rel_parent_dir_path = get_norm_path(parent_dir_path)
        rel_dir_path = get_norm_path(parent_dir_path, child_name=dirname)
        abs_dir_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path, child_name=dirname)

        # Ensure directory does not exist
        if os.path.exists(abs_dir_path) and os.path.isdir(abs_dir_path):
            raise DirectoryAlreadyExistError(f"Cannot create directory='{rel_dir_path}'.")

        await aiofiles.os.makedirs(abs_dir_path, exist_ok=False)

        return DirectoryEntity(
            dirname=dirname,
            parent_dir_path=rel_parent_dir_path,
        )

    async def delete_by_dirname_and_parent_dir_path(self, dirname: str, parent_dir_path: str) -> None:
        """
        Recursively remove a directory and its contents.

        Parameters:
            dirname (str): Name of the directory to delete.
            parent_dir_path (str): Relative parent directory path.

        Raises:
            DirectoryNotExistError: If the directory does not exist.
        """

        # Build relative and absolute paths
        rel_dir_path = get_norm_path(parent_dir_path, child_name=dirname)
        abs_dir_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path, child_name=dirname)

        # Ensure directory exists
        if not os.path.exists(abs_dir_path) or not os.path.isdir(abs_dir_path):
            raise DirectoryNotExistError(f"Cannot delete directory='{rel_dir_path}'.")

        await aioshutil.rmtree(abs_dir_path, ignore_errors=True)

    async def list_by_parent_dir_path(self, parent_dir_path: str) -> tuple[list[FileEntity], list[DirectoryEntity]]:
        """
        List files and subdirectories under the given directory.

        Parameters:
            parent_dir_path (str): Relative path of the directory to list.

        Returns:
            tuple[list[FileEntity], list[DirectoryEntity]]: Two lists: FileEntity list and DirectoryEntity list.

        Raises:
            DirectoryNotExistError: If the target directory does not exist.
        """

        # Build relative and absolute paths
        rel_parent_dir_path = get_norm_path(parent_dir_path)
        abs_parent_dir_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path)

        # Ensure directory exists
        if not os.path.exists(abs_parent_dir_path) or not os.path.isdir(abs_parent_dir_path):
            raise DirectoryNotExistError(f"Cannot list directory='{rel_parent_dir_path}'.")

        file_entities = []
        directory_entities = []
        entry_names = await aiofiles.os.listdir(abs_parent_dir_path)

        for entry_name in entry_names:
            abs_entry_path = get_norm_path(parent_dir_path, prefix=self.shared_dir_path, child_name=entry_name)

            if os.path.isfile(abs_entry_path):
                file_entity = FileEntity(
                    filename=entry_name,
                    parent_dir_path=rel_parent_dir_path,
                    size=os.path.getsize(abs_entry_path),
                    modified_at=get_datetime_from_timestamp(os.path.getmtime(abs_entry_path)),
                )

                file_entities.append(file_entity)

            else:
                directory_entity = DirectoryEntity(
                    dirname=entry_name,
                    parent_dir_path=rel_parent_dir_path,
                )

                directory_entities.append(directory_entity)

        return file_entities, directory_entities
