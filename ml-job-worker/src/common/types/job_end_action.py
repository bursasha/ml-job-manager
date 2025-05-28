from enum import StrEnum


class JobEndActionType(StrEnum):
    """
    Enumeration type of possible job end actions.
    """

    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
