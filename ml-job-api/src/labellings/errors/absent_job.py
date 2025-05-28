from src.common.errors import BaseError


class LabellingAbsentJobError(BaseError):
    """
    Raised when attempting to create one or more labelling records with a `job_id` that does not exist in the system.
    """

    message = "Labelling associated job is absent."
