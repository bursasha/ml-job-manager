import os
from typing import Any

import h5py
import numpy as np
from astropy.io import fits
from numpy.typing import NDArray
from sklearn.preprocessing import minmax_scale

from src.data_preprocessing.config import DataPreprocessingConfig


#


def read_spectrum_file(file_path: str) -> dict[str, Any]:
    """
    Read a single FITS spectrum file.

    Opens the FITS file at `file_path`, extracts the header and data arrays, and returns a dict with:
      - "filename": the FILENAME header value,
      - "wave": the wavelength array (data[2]),
      - "flux": the flux array (data[0]).

    Parameters:
        file_path (str): Absolute path to the FITS file.

    Returns:
        dict[str, Any]: A mapping with keys "filename", "wave", and "flux".
    """

    with fits.open(file_path) as hdul_reader:
        header = hdul_reader[0].header
        data = hdul_reader[0].data
        raw_spectrum = dict(
            filename=header["FILENAME"],
            wave=data[2],
            flux=data[0],
        )

    return raw_spectrum


def write_preprocessed_file(
    file_path: str, filenames: NDArray[str], fluxes: NDArray[float], wave: NDArray[float]
) -> None:
    """
    Write preprocessed spectra data to an HDF5 file.

    Creates three datasets in the HDF5 at `file_path`:
      - "filenames": array of UTF-8–encoded spectrum filenames,
      - "fluxes": 2D array of scaled flux values,
      - "wave": 1D array of the common wavelength grid.

    Parameters:
        file_path (str): Path where to create the HDF5 file.
        filenames (NDArray[str]): 1D array of spectrum filenames.
        fluxes (NDArray[float]): 2D array of shape (n_spectra, n_wavepoints) of scaled fluxes.
        wave (NDArray[float]): 1D array of the common wavelength grid.
    """

    with h5py.File(file_path, "w") as h5f_writer:
        h5f_writer.create_dataset("filenames", data=filenames.tolist(), dtype=h5py.string_dtype(encoding="utf-8"))
        h5f_writer.create_dataset("fluxes", data=fluxes)
        h5f_writer.create_dataset("wave", data=wave)


#


def preprocess_data_dir(
    data_dir_path: str, wave_start_point: float, wave_end_point: float, wave_point_count: int
) -> tuple[NDArray[str], NDArray[float], NDArray[float]]:
    """
    Scan a directory of FITS spectra, interpolate and scale their flux arrays.

    1. Builds a uniform wavelength grid from `wave_start_point` to `wave_end_point` with `wave_point_count` points.
    2. Iterates over all files in `data_dir_path`, reading each spectrum.
    3. Interpolates each spectrum’s flux onto the uniform grid.
    4. Stacks the filenames, fluxes, and returns them along with the wave grid.

    Parameters:
        data_dir_path (str): Directory containing raw FITS files.
        wave_start_point (float): Minimum wavelength (Å) of the output grid.
        wave_end_point (float): Maximum wavelength (Å) of the output grid.
        wave_point_count (int): Number of points in the output grid.

    Returns:
        Tuple[NDArray[str], NDArray[float], NDArray[float]]:
            1D array of spectrum filenames,
            2D array (n_spectra × wave_point_count) of scaled fluxes,
            1D array (wave_point_count) of the uniform wavelength grid.
    """

    filenames = []
    fluxes = []
    uniform_wave = np.linspace(wave_start_point, wave_end_point, wave_point_count, dtype=float)

    with os.scandir(data_dir_path) as spectrum_files:
        for spectrum_file in spectrum_files:
            spectrum_file_data = read_spectrum_file(spectrum_file.path)
            interpolated_flux = np.interp(uniform_wave, spectrum_file_data["wave"], spectrum_file_data["flux"])

            filenames.append(spectrum_file_data["filename"])
            fluxes.append(interpolated_flux)

    prepared_filenames = np.array(filenames, dtype=str)
    interpolated_fluxes = minmax_scale(np.array(fluxes, dtype=float), feature_range=(-1, 1), axis=1)

    return prepared_filenames, interpolated_fluxes, uniform_wave


#


def run(config: DataPreprocessingConfig) -> None:
    """
    Execute the full preprocessing workflow.

    1. Calls `preprocess_data_dir` with configuration parameters to obtain filenames,
        scaled fluxes, and the common wavelength grid.
    2. Writes the results to the HDF5 file at `config.result_file_path`.

    Parameters:
        config (DataPreprocessingConfig): Validated configuration object containing all job parameters.
    """

    filenames, fluxes, wave = preprocess_data_dir(
        config.data_dir_path, config.wave_start_point, config.wave_end_point, config.wave_point_count
    )

    write_preprocessed_file(config.result_file_path, filenames, fluxes, wave)
