"""
Centralized entity metadata definitions.
"""

labelling_resources = {
    "labelling_id": {
        "DESCRIPTION": "Unique identifier of the labelling",
    },
    "job_id": {
        "DESCRIPTION": "Identifier of the associated job",
    },
    "spectrum_filename": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 70,
        "DESCRIPTION": "Filename of the associated spectrum",
        "EXAMPLES": ["spec-56207-M31011N44B2_sp01-006.fits"],
    },
    "spectrum_set": {
        "DESCRIPTION": "Dataset group in which this spectrum is evaluated for the current associated job",
    },
    "sequence_iteration": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Zero‑based index of the Active ML job iteration in some associated job sequence",
        "EXAMPLES": [0],
    },
    "model_prediction": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 30,
        "DESCRIPTION": "Prediction output by the model for this spectrum",
        "EXAMPLES": ["double-peak"],
    },
    "user_label": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 30,
        "DESCRIPTION": "Label assigned by the user",
        "EXAMPLES": ["single-peak"],
    },
    "user_comment": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 50,
        "DESCRIPTION": "Comment provided by the user during labelling",
        "EXAMPLES": ["High noise level"],
    },
}

list_resources = {
    "job_id": {
        "DESCRIPTION": "Identifier of the job for which labellings are listed",
    },
    "total": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Total number of associated labellings",
        "EXAMPLES": [1],
    },
    "labellings": {
        "DESCRIPTION": "List of associated labelling records",
    },
}
