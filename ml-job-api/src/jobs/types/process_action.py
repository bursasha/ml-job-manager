from enum import StrEnum


class ProcessActionType(StrEnum):
    """
    Enumeration type of actions that can be applied to a pending job.
    """

    RUN = "RUN"
    ABORT = "ABORT"
