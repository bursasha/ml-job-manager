import os
from datetime import (
    datetime,
    timezone,
)
from uuid import (
    UUID,
    uuid4,
)


#


def generate_uuid() -> UUID:
    """
    Generate a new random UUID4.

    Returns:
        UUID: A version-4 UUID suitable for unique identifiers.
    """

    return uuid4()


#


def get_current_utc_datetime() -> datetime:
    """
    Get the current time in UTC.

    Returns:
        datetime: A timezone-aware datetime object set to UTC now.
    """

    return datetime.now(timezone.utc)


def get_duration_in_seconds(start: datetime, end: datetime) -> float:
    """
    Compute the duration in seconds between two datetimes.

    Parameters:
        start (datetime): The starting datetime.
        end (datetime): The ending datetime.

    Returns:
        float: The total number of seconds between `start` and `end`.
    """

    return (end - start).total_seconds()


def get_datetime_from_timestamp(timestamp: float) -> datetime:
    """
    Convert a POSIX timestamp to a UTC datetime.

    Parameters:
        timestamp (float): Seconds since the Unix epoch.

    Returns:
        datetime: A timezone-aware UTC datetime corresponding to `timestamp`.
    """

    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


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
