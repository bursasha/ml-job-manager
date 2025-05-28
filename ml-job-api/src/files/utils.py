from typing import AsyncIterator

import aiofiles
from fastapi import UploadFile


#


async def upload_file(file_path: str, file: UploadFile, chunk_size: int) -> None:
    """
    Stream an incoming UploadFile to disk in configurable chunks.

    Reads `chunk_size` bytes at a time from the FastAPI `UploadFile` and writes them
    to the local filesystem at `file_path`. This approach prevents loading the entire
    file into memory.

    Parameters:
        file_path (str): The absolute path where the uploaded file will be saved.
        file (UploadFile): The incoming file object provided by FastAPI for multipart uploads.
        chunk_size (int): Number of bytes to read and write per iteration.
    """

    async with aiofiles.open(file_path, "wb") as file_writer:
        while chunk := await file.read(chunk_size):
            await file_writer.write(chunk)


async def download_file(file_path: str, chunk_size: int) -> AsyncIterator[bytes]:
    """
    Stream a local file from disk back to the caller in configurable chunks.

    Opens the file at `file_path` for binary reading and yields `chunk_size` bytes
    at a time. This iterator can be directly returned as a StreamingResponse in FastAPI.

    Parameters:
        file_path (str): The absolute or relative path of the file to be streamed.
        chunk_size (int): Number of bytes to read and yield per iteration.

    Returns:
        AsyncIterator[bytes]: An asynchronous iterator yielding byte chunks of the file.
    """

    async with aiofiles.open(file_path, "rb") as file_reader:
        while chunk := await file_reader.read(chunk_size):
            yield chunk
