"""
Centralized entity metadata definitions.
"""

spectrum_resources = {
    "filename": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 70,
        "PATTERN": r"^spec-\d+-[A-Za-z0-9]+_sp\d+-\d+\.fits$",
        "DESCRIPTION": "Name of the FITS file containing the spectrum, following the LAMOST naming convention",
        "EXAMPLES": ["spec-56207-M31011N44B2_sp01-006.fits"],
    },
    "targetname": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 70,
        "DESCRIPTION": "Target designation from the input catalog (DESIG header key)",
        "EXAMPLES": ["LAMOST J192438.86+365628.7"],
    },
    "observed_at": {
        "DESCRIPTION": "UTC datetime of the observation (DATE-OBS header key)",
        "EXAMPLES": ["2025-04-04T12:00:00Z"],
    },
    "type": {
        "DESCRIPTION": "Broad spectral class (CLASS header key)",
    },
    "subtype": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 30,
        "DESCRIPTION": "Detailed spectral subtype (SUBCLASS header key)",
        "EXAMPLES": ["G2V"],
    },
    "ra": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Right ascension in decimal degrees from the input catalog (RA header key)",
        "EXAMPLES": [291.161958],
    },
    "dec": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Declination in decimal degrees from the input catalog (DEC header key)",
        "EXAMPLES": [36.941333],
    },
    "magtype": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 20,
        "DESCRIPTION": "Magnitude type identifier (MAGTYPE header key)",
        "EXAMPLES": ["Kp"],
    },
    "mag_1": {
        "MIN_VALUE": 0,
        "MAX_VALUE": 100,
        "DESCRIPTION": "Magnitude in band 1 (MAG1 header key)",
        "EXAMPLES": [15.67],
    },
    "mag_2": {
        "MIN_VALUE": 0,
        "MAX_VALUE": 100,
        "DESCRIPTION": "Magnitude in band 2 (MAG2 header key)",
        "EXAMPLES": [99.00],
    },
    "mag_3": {
        "MIN_VALUE": 0,
        "MAX_VALUE": 100,
        "DESCRIPTION": "Magnitude in band 3 (MAG3 header key)",
        "EXAMPLES": [99.00],
    },
    "mag_4": {
        "MIN_VALUE": 0,
        "MAX_VALUE": 100,
        "DESCRIPTION": "Magnitude in band 4 (MAG4 header key)",
        "EXAMPLES": [99.00],
    },
    "mag_5": {
        "MIN_VALUE": 0,
        "MAX_VALUE": 100,
        "DESCRIPTION": "Magnitude in band 5 (MAG5 header key)",
        "EXAMPLES": [99.00],
    },
    "mag_6": {
        "MIN_VALUE": 0,
        "MAX_VALUE": 100,
        "DESCRIPTION": "Magnitude in band 6 (MAG6 header key)",
        "EXAMPLES": [99.00],
    },
    "mag_7": {
        "MIN_VALUE": 0,
        "MAX_VALUE": 100,
        "DESCRIPTION": "Magnitude in band 7 (MAG7 header key)",
        "EXAMPLES": [99.00],
    },
    "sn_u": {
        "DESCRIPTION": "Signal‑to‑noise ratio in the u band (SN_U header key)",
        "EXAMPLES": [1.26],
    },
    "sn_g": {
        "DESCRIPTION": "Signal‑to‑noise ratio in the g band (SN_G header key)",
        "EXAMPLES": [6.29],
    },
    "sn_r": {
        "DESCRIPTION": "Signal‑to‑noise ratio in the r band (SN_R header key)",
        "EXAMPLES": [17.65],
    },
    "sn_i": {
        "DESCRIPTION": "Signal‑to‑noise ratio in the i band (SN_I header key)",
        "EXAMPLES": [22.46],
    },
    "sn_z": {
        "DESCRIPTION": "Signal‑to‑noise ratio in the z band (SN_Z header key)",
        "EXAMPLES": [16.34],
    },
    "z": {
        "DESCRIPTION": "Measured redshift from the spectrum (Z header key)",
        "EXAMPLES": [-0.00032162],
    },
    "z_err": {
        "DESCRIPTION": "Uncertainty of the measured redshift (Z_ERR header key)",
        "EXAMPLES": [0.0000021],
    },
    "wave": {
        "DESCRIPTION": "Wavelength array in angstroms from the FITS data",
        "EXAMPLES": [[3690.0, 3691.0, 3692.0]],
    },
    "flux": {
        "DESCRIPTION": "Flux array in 10⁻¹⁷ erg s⁻¹ cm⁻² Å⁻¹ from the FITS data",
        "EXAMPLES": [[1.23, 1.19, 1.15]],
    },
}
