from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)

from src.spectra.resources import spectrum_resources
from src.spectra.types import SpectrumType


class SpectrumReadSerializer(BaseModel):
    """
    Serializer model for a retrieved LAMOST spectrum.
    """

    filename: str = Field(
        ...,
        description=spectrum_resources["filename"]["DESCRIPTION"],
        examples=spectrum_resources["filename"]["EXAMPLES"],
    )

    targetname: str = Field(
        ...,
        description=spectrum_resources["targetname"]["DESCRIPTION"],
        examples=spectrum_resources["targetname"]["EXAMPLES"],
    )

    observed_at: datetime = Field(
        ...,
        description=spectrum_resources["observed_at"]["DESCRIPTION"],
        examples=spectrum_resources["observed_at"]["EXAMPLES"],
    )

    type: SpectrumType = Field(
        ...,
        description=spectrum_resources["type"]["DESCRIPTION"],
    )

    subtype: str = Field(
        ...,
        description=spectrum_resources["subtype"]["DESCRIPTION"],
        examples=spectrum_resources["subtype"]["EXAMPLES"],
    )

    ra: float = Field(
        ...,
        description=spectrum_resources["ra"]["DESCRIPTION"],
        examples=spectrum_resources["ra"]["EXAMPLES"],
    )

    dec: float = Field(
        ...,
        description=spectrum_resources["dec"]["DESCRIPTION"],
        examples=spectrum_resources["dec"]["EXAMPLES"],
    )

    magtype: str = Field(
        ...,
        description=spectrum_resources["magtype"]["DESCRIPTION"],
        examples=spectrum_resources["magtype"]["EXAMPLES"],
    )

    mag_1: float = Field(
        ...,
        description=spectrum_resources["mag_1"]["DESCRIPTION"],
        examples=spectrum_resources["mag_1"]["EXAMPLES"],
    )

    mag_2: float = Field(
        ...,
        description=spectrum_resources["mag_2"]["DESCRIPTION"],
        examples=spectrum_resources["mag_2"]["EXAMPLES"],
    )

    mag_3: float = Field(
        ...,
        description=spectrum_resources["mag_3"]["DESCRIPTION"],
        examples=spectrum_resources["mag_3"]["EXAMPLES"],
    )

    mag_4: float = Field(
        ...,
        description=spectrum_resources["mag_4"]["DESCRIPTION"],
        examples=spectrum_resources["mag_4"]["EXAMPLES"],
    )

    mag_5: float = Field(
        ...,
        description=spectrum_resources["mag_5"]["DESCRIPTION"],
        examples=spectrum_resources["mag_5"]["EXAMPLES"],
    )

    mag_6: float = Field(
        ...,
        description=spectrum_resources["mag_6"]["DESCRIPTION"],
        examples=spectrum_resources["mag_6"]["EXAMPLES"],
    )

    mag_7: float = Field(
        ...,
        description=spectrum_resources["mag_7"]["DESCRIPTION"],
        examples=spectrum_resources["mag_7"]["EXAMPLES"],
    )

    sn_u: float = Field(
        ...,
        description=spectrum_resources["sn_u"]["DESCRIPTION"],
        examples=spectrum_resources["sn_u"]["EXAMPLES"],
    )

    sn_g: float = Field(
        ...,
        description=spectrum_resources["sn_g"]["DESCRIPTION"],
        examples=spectrum_resources["sn_g"]["EXAMPLES"],
    )

    sn_r: float = Field(
        ...,
        description=spectrum_resources["sn_r"]["DESCRIPTION"],
        examples=spectrum_resources["sn_r"]["EXAMPLES"],
    )

    sn_i: float = Field(
        ...,
        description=spectrum_resources["sn_i"]["DESCRIPTION"],
        examples=spectrum_resources["sn_i"]["EXAMPLES"],
    )

    sn_z: float = Field(
        ...,
        description=spectrum_resources["sn_z"]["DESCRIPTION"],
        examples=spectrum_resources["sn_z"]["EXAMPLES"],
    )

    z: float = Field(
        ...,
        description=spectrum_resources["z"]["DESCRIPTION"],
        examples=spectrum_resources["z"]["EXAMPLES"],
    )

    z_err: float = Field(
        ...,
        description=spectrum_resources["z_err"]["DESCRIPTION"],
        examples=spectrum_resources["z_err"]["EXAMPLES"],
    )

    wave: list[float] = Field(
        ...,
        description=spectrum_resources["wave"]["DESCRIPTION"],
        examples=spectrum_resources["wave"]["EXAMPLES"],
    )

    flux: list[float] = Field(
        ...,
        description=spectrum_resources["flux"]["DESCRIPTION"],
        examples=spectrum_resources["flux"]["EXAMPLES"],
    )
