from enum import StrEnum


class LabellingSpectrumSetType(StrEnum):
    """
    Enumeration type of the different dataset partitions in an Active ML labelling workflow.
    """

    CANDIDATE = "CANDIDATE"
    PERFORMANCE_ESTIMATION = "PERFORMANCE_ESTIMATION"
    ORACLE = "ORACLE"
