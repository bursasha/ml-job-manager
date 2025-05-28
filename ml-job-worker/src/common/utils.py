import json
import os
import traceback
from datetime import (
    datetime,
    timezone,
)
from typing import Any


#


def get_current_utc_datetime() -> datetime:
    """
    Get the current time in UTC.

    Returns:
        datetime: A timezone-aware datetime object set to UTC now.
    """

    return datetime.now(timezone.utc)


#


def get_error_log() -> str:
    """
    Capture and return the stack trace of the most recently handled exception.

    Returns:
        str: A formatted string containing the traceback of the last exception.
    """

    return traceback.format_exc()


#


def get_norm_path(parent_path: str, prefix: str | None = None, child_name: str | None = None) -> str:
    """
    Build and normalize a filesystem path, optionally prepending a prefix and appending a child name.

    The resulting path is processed with os.path.normpath to collapse redundant separators
    and up-level references.

    Parameters:
        parent_path (str): Base path segment, which may be relative or absolute.
        prefix (str | None):
            Optional path to prepend before `parent_path`. If provided, leading slashes in
            `parent_path` are stripped before joining.
        child_name (str | None): Optional final segment to append after the combined prefix and parent.

    Returns:
        str: The normalized filesystem path.
    """

    parts = []

    if prefix:
        parts.append(prefix)

        parent_path = parent_path.lstrip("\\/")

    parts.append(parent_path)

    if child_name:
        parts.append(child_name)

    path = os.path.join(*parts)
    norm_path = os.path.normpath(path)

    return norm_path


#


def read_config_file(file_path: str) -> dict[str, Any]:
    """
    Load a JSON configuration file and return its contents as a Python dict.

    Parameters:
        file_path (str): Path to the JSON file to read.

    Returns:
        dict[str, Any]: Parsed JSON config content.
    """

    with open(file_path, "r") as file_reader:
        raw_config = json.load(file_reader)

    return raw_config


def write_log_file(file_path: str, log: str) -> None:
    """
    Write a string log to a file, overwriting any existing content.

    Parameters:
        file_path (str): Destination path for the log file.
        log (str): String content to write.
    """

    with open(file_path, "w") as file_writer:
        file_writer.write(log)
