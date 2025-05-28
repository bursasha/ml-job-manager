from src.common.errors import BaseError


class LabellingNotExistError(BaseError):
    """
    Raised when a requested labelling record cannot be found by its ID.
    """

    message = "Labelling does not exist."
