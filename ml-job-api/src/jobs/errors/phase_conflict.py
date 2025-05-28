from src.common.errors import BaseError


class JobPhaseConflictError(BaseError):
    """
    Raised when an operation is not allowed in the job’s current lifecycle phase.
    """

    message = "Job phase conflict."
