from enum import StrEnum


class JobType(StrEnum):
    """
    Enumeration type of supported ML job types.
    """

    DATA_PREPROCESSING = "DATA_PREPROCESSING"
    ACTIVE_ML = "ACTIVE_ML"
