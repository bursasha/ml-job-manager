from enum import StrEnum


class PhaseType(StrEnum):
    """
    Enumeration type of job lifecycle phases.
    """

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    ABORTED = "ABORTED"
