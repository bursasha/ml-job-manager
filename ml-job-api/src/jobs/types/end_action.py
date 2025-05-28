from enum import StrEnum


class EndActionType(StrEnum):
    """
    Enumeration type of possible job end actions.
    """

    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
