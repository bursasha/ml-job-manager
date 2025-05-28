from src.common.errors import BaseError


class DirectoryAlreadyExistError(BaseError):
    """
    Raised when attempting to create a directory that already exists.
    """

    message = "Directory already exists."
