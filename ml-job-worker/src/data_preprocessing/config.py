from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class DataPreprocessingConfig(BaseModel):
    """
    Configuration settings for the data preprocessing pipeline.

    This model defines the input parameters for scanning a directory of raw FITS spectra,
    interpolating each spectrum’s flux values onto a uniform wavelength grid, and writing
    the results to an HDF5 file. All values may be loaded from a JSON configuration file.
    """

    model_config = ConfigDict(from_attributes=True)

    data_dir_path: str = Field(
        ...,
        description="Path to the directory containing raw FITS spectrum files for preprocessing",
        examples=["/B6001"],
    )

    wave_start_point: float = Field(
        ...,
        description="Starting wavelength in angstroms of the uniform output wave grid for fluxes interpolation",
        examples=[5000],
    )

    wave_end_point: float = Field(
        ...,
        description="Ending wavelength in angstroms of the uniform output wave grid for fluxes interpolation",
        examples=[8000],
    )

    wave_point_count: int = Field(
        ...,
        description="Point number in the output wave grid: how many fluxes will be interpolated for each spectrum",
        examples=[140],
    )

    result_file_path: str | None = Field(
        None,
        description="Path to the output HDF5 file where preprocessed data: filenames, fluxes, wave, will be saved",
        examples=["/job_lamost_2025_v883_orionis_spectra_learning_82b2b3c4-f5c1-4774-9a9e-f917998d7935/result.h5"],
    )
