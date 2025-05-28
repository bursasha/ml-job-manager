from src.common.errors import BaseError


class FileNotExistError(BaseError):
    """
    Raised when attempting to access or delete a file that does not exist.
    """

    message = "File does not exist."


class DirectoryNotExistError(BaseError):
    """
    Raised when attempting to access, list, or delete a directory that does not exist.
    """

    message = "Directory does not exist."
