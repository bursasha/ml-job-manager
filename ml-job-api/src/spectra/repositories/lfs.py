import asyncio
import os

from src.common.utils import get_norm_path
from src.spectra.entity import SpectrumEntity
from src.spectra.errors import SpectrumNotExistError
from src.spectra.repository import SpectrumRepository
from src.spectra.utils import read_file


class SpectrumLFSRepository(SpectrumRepository):
    """
    Local filesystem implementation of SpectrumRepository.
    """

    def __init__(self, lfs_spectra_dir_path: str) -> None:
        """
        Initialize the repository with the base path to spectra storage.

        Parameters:
            lfs_spectra_dir_path (str): Absolute path to the root of the shared spectra directory.
        """

        self.shared_dir_path = lfs_spectra_dir_path

    @staticmethod
    def _get_dir_path(filename: str) -> str:
        """
        Compute the relative directory path for a given FITS filename.

        LAMOST filenames encode their subdirectory in the third dash-
        separated segment, before the underscore.

        Parameters:
            filename (str): A LAMOST FITS filename, e.g. "spec-56207-M31011N44B2_sp01-006.fits".

        Returns:
            str:
                A relative path of the form "/<dirname>", where dirname
                is extracted from the filename, e.g. "/M31011N44B2".
        """

        dirname = filename.split("-")[2].split("_")[0]
        dir_path = get_norm_path(f"/{dirname}")

        return dir_path

    async def get_by_filename(self, filename: str) -> SpectrumEntity:
        """
        Retrieve and parse a spectrum entity by its FITS filename from the LFS.

        Builds the absolute file path under the shared directory, checks
        for existence and file-type, then offloads the FITS reading and
        parsing to a background thread.

        Parameters:
            filename (str): The FITS filename to retrieve, following the LAMOST naming convention.

        Returns:
            SpectrumEntity: An entity model populated with header metadata and data arrays.

        Raises:
            SpectrumNotExistError: If the file does not exist or is not a regular file.
        """

        # Build relative and absolute paths
        rel_parent_dir_path = self._get_dir_path(filename)
        rel_file_path = get_norm_path(rel_parent_dir_path, child_name=filename)
        abs_file_path = get_norm_path(rel_parent_dir_path, prefix=self.shared_dir_path, child_name=filename)

        # Ensure file exists
        if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
            raise SpectrumNotExistError(f"Cannot get spectrum from file='{rel_file_path}'.")

        spectrum_file_data = await asyncio.to_thread(read_file, abs_file_path)

        return SpectrumEntity.model_validate(spectrum_file_data)
