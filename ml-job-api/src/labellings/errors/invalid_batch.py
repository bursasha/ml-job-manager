from src.common.errors import BaseError


class LabellingInvalidBatchError(BaseError):
    """
    Raised when the provided lists of labelling IDs and edit payloads do not match during a batch update operation.
    """

    message = "Labelling invalid batch."
