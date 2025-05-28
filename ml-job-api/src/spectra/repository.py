from abc import (
    ABC,
    abstractmethod,
)

from src.spectra.entity import SpectrumEntity


class SpectrumRepository(ABC):
    """
    Repository interface for working with spectral data.
    """

    @abstractmethod
    async def get_by_filename(self, filename: str) -> SpectrumEntity:
        """
        Retrieve and parse a spectrum entity by its FITS filename.

        Parameters:
            filename (str): The exact FITS filename of the spectrum to retrieve, following the LAMOST naming convention.

        Returns:
            SpectrumEntity:
                A fully validated entity model containing all header metadata
                and data arrays for that spectrum.
        """

        raise NotImplementedError
