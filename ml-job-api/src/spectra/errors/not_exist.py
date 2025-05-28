from src.common.errors import BaseError


class SpectrumNotExistError(BaseError):
    """
    Raised when a requested spectrum file cannot be found or accessed.
    """

    message = "Spectrum does not exist."
