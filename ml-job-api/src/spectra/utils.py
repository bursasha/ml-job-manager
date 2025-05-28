from typing import Any

from astropy.io import fits


#


def read_file(file_path: str) -> dict[str, Any]:
    """
    Read a LAMOST FITS spectrum file and extract its header metadata and data arrays.

    This function opens the FITS file at `file_path`, reads the primary header and data,
    and returns a dictionary containing:
      - filename: FITS header "FILENAME"
      - targetname: FITS header "DESIG"
      - observed_at: FITS header "DATE-OBS"
      - type: FITS header "CLASS"
      - subtype: FITS header "SUBCLASS"
      - ra: FITS header "RA" (right ascension in decimal degrees)
      - dec: FITS header "DEC" (declination in decimal degrees)
      - magtype: FITS header "MAGTYPE"
      - mag_1…mag_7: FITS headers "MAG1" through "MAG7"
      - sn_u…sn_z: FITS headers "SN_U" through "SN_Z" (signal-to-noise ratios)
      - z: FITS header "Z" (redshift)
      - z_err: FITS header "Z_ERR" (redshift uncertainty)
      - wave: wavelength array (from HDU data index 2), as a Python list of floats
      - flux: flux array (from HDU data index 0), as a Python list of floats

    Parameters:
        file_path (str): Path to the FITS file to read.

    Returns:
        dict[str, Any]: A dictionary mapping metadata and data arrays extracted from the file.
    """

    with fits.open(file_path) as hdul_reader:
        header = hdul_reader[0].header
        data = hdul_reader[0].data
        raw_spectrum = dict(
            filename=header["FILENAME"],
            targetname=header["DESIG"],
            observed_at=header["DATE-OBS"],
            type=header["CLASS"],
            subtype=header["SUBCLASS"],
            ra=header["RA"],
            dec=header["DEC"],
            magtype=header["MAGTYPE"],
            mag_1=header["MAG1"],
            mag_2=header["MAG2"],
            mag_3=header["MAG3"],
            mag_4=header["MAG4"],
            mag_5=header["MAG5"],
            mag_6=header["MAG6"],
            mag_7=header["MAG7"],
            sn_u=header["SN_U"],
            sn_g=header["SN_G"],
            sn_r=header["SN_R"],
            sn_i=header["SN_I"],
            sn_z=header["SN_Z"],
            z=header["Z"],
            z_err=header["Z_ERR"],
            wave=data[2].tolist(),
            flux=data[0].tolist(),
        )

    return raw_spectrum
