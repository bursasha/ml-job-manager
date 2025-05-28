from src.common.errors import BaseError


class JobNotExistError(BaseError):
    """
    Raised when the requested job cannot be found in the data store.
    """

    message = "Job does not exist."
