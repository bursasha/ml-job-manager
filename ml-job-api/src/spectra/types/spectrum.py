from enum import StrEnum


class SpectrumType(StrEnum):
    """
    Enumeration type of broad spectral classes for LAMOST spectra.
    """

    STAR = "STAR"
    GALAXY = "GALAXY"
    QSO = "QSO"
    UNKNOWN = "UNKNOWN"
