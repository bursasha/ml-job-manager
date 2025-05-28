from src.infrastructure.storages import lfs_spectra_dir_path
from src.spectra.repositories import SpectrumLFSRepository
from src.spectra.service import SpectrumService


def get_service_using_lfs() -> SpectrumService:
    """
    Build and return a SpectrumService backed by a local filesystem repository.

    This function constructs a SpectrumLFSRepository using the configured
    shared spectra directory path, then injects it into a SpectrumService.

    Returns:
        SpectrumService:
            Service instance for handling spectral data operations from the local filesystem.
    """

    lfs_repository = SpectrumLFSRepository(lfs_spectra_dir_path)

    return SpectrumService(lfs_repository)
