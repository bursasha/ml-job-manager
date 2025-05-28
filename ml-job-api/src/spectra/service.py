from src.spectra.repository import SpectrumRepository
from src.spectra.serializers import SpectrumReadSerializer


class SpectrumService:
    """
    Business logic layer for working with spectral data.
    """

    def __init__(self, repository: SpectrumRepository) -> None:
        """
        Initialize the spectrum service with a repository implementation.

        Parameters:
            repository (SpectrumRepository): Concrete repository for accessing spectral data.
        """

        self.repository = repository

    async def retrieve_spectrum_by_filename(self, filename: str) -> SpectrumReadSerializer:
        """
        Retrieve and serialize a spectrum by its FITS filename.

        This method fetches the raw SpectrumEntity from the repository,
        then constructs a SpectrumReadSerializer for API responses.

        Parameters:
            filename (str): The FITS filename to retrieve, following the LAMOST naming convention.

        Returns:
            SpectrumReadSerializer: The serialized spectrum data ready for API output.
        """

        entity = await self.repository.get_by_filename(filename)

        return SpectrumReadSerializer(**entity.model_dump())
