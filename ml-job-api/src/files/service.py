from typing import AsyncIterator

from fastapi import UploadFile

from src.files.params import (
    EntryListParams,
    EntryLocateParams,
)
from src.files.repository import FileRepository
from src.files.serializers import (
    DirectoryReadSerializer,
    DirectorySummarizeSerializer,
    EntryListSerializer,
    FileReadSerializer,
    FileSummarizeSerializer,
)


class FileService:
    """
    Business logic layer for managing file and directory operations.
    """

    def __init__(self, repository: FileRepository) -> None:
        """
        Initialize the file service with a repository implementation.

        Parameters:
            repository (FileRepository): Concrete repository for performing file and directory operations.
        """

        self.repository = repository

    async def upload_file_by_filename(
        self, filename: str, params: EntryLocateParams, file: UploadFile
    ) -> FileReadSerializer:
        """
        Upload a file to storage and return its metadata.

        Parameters:
            filename (str): Desired name under which to store the file.
            params (EntryLocateParams): Query parameters specifying the target directory.
            file (UploadFile): The file object received via FastAPI multipart upload.

        Returns:
            FileReadSerializer: Serializer containing metadata of the stored file.
        """

        entity = await self.repository.upload_by_filename_and_parent_dir_path(filename, params.parent_dir_path, file)

        return FileReadSerializer(**entity.model_dump())

    async def download_file_by_filename(self, filename: str, params: EntryLocateParams) -> AsyncIterator[bytes]:
        """
        Stream a stored file's contents back to the client.

        Parameters:
            filename (str): Name of the file to retrieve.
            params (EntryLocateParams): Query parameters specifying the directory containing the file.

        Returns:
            AsyncIterator[bytes]: An asynchronous iterator yielding chunks of the file's bytes.
        """

        return await self.repository.download_by_filename_and_parent_dir_path(filename, params.parent_dir_path)

    async def remove_file_by_filename(self, filename: str, params: EntryLocateParams) -> None:
        """
        Remove a file from storage.

        Parameters:
            filename (str): Name of the file to delete.
            params (EntryLocateParams): Query parameters specifying the directory containing the file.
        """

        await self.repository.delete_by_filename_and_parent_dir_path(filename, params.parent_dir_path)

    async def initialize_directory_by_dirname(self, dirname: str, params: EntryLocateParams) -> DirectoryReadSerializer:
        """
        Create a new directory in storage and return its metadata.

        Parameters:
            dirname (str): Name of the directory to create.
            params (EntryLocateParams): Query parameters specifying the parent directory.

        Returns:
            DirectoryReadSerializer: Serializer representing the created directory.
        """

        entity = await self.repository.create_by_dirname_and_parent_dir_path(dirname, params.parent_dir_path)

        return DirectoryReadSerializer(**entity.model_dump())

    async def remove_directory_by_dirname(self, dirname: str, params: EntryLocateParams) -> None:
        """
        Recursively remove a directory and its contents from storage.

        Parameters:
            dirname (str): Name of the directory to delete.
            params (EntryLocateParams): Query parameters specifying the parent directory.
        """

        await self.repository.delete_by_dirname_and_parent_dir_path(dirname, params.parent_dir_path)

    async def list_entries(self, params: EntryListParams) -> EntryListSerializer:
        """
        List all files and subdirectories under a given directory.

        This method retrieves raw FileEntity and DirectoryEntity lists from the repository,
        converts them to FileSummarizeSerializer and DirectorySummarizeSerializer,
        and returns an EntryListSerializer containing counts and summaries.

        Parameters:
            params (EntryListParams): Query parameters specifying the directory to list.

        Returns:
            EntryListSerializer: Serializer containing listing metadata of the directory contents.
        """

        file_entities, directory_entities = await self.repository.list_by_parent_dir_path(params.parent_dir_path)
        file_serializers = [FileSummarizeSerializer(**file_entity.model_dump()) for file_entity in file_entities]
        directory_serializers = [
            DirectorySummarizeSerializer(**directory_entity.model_dump()) for directory_entity in directory_entities
        ]
        file_count = len(file_serializers)
        directory_count = len(directory_serializers)
        total = file_count + directory_count

        return EntryListSerializer(
            parent_dir_path=params.parent_dir_path,
            total=total,
            file_count=file_count,
            directory_count=directory_count,
            files=file_serializers,
            directories=directory_serializers,
        )
