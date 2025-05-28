"""
Centralized entity metadata definitions.
"""

job_resources = {
    "job_id": {
        "DESCRIPTION": "Unique identifier of the job",
    },
    "dir_path": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 255,
        "PATTERN": r"^(?:[\\/](?:[^\\/]+(?:[\\/][^\\/]+)*)?)$",
        "DESCRIPTION": "Storage directory path where job data/outputs are stored",
        "EXAMPLES": ["/JOBS/job_lamost_2025_v883_orionis_spectra_learning_3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    },
    "type": {
        "DESCRIPTION": "Job category indicating its functional purpose",
    },
    "phase": {
        "DESCRIPTION": "Current lifecycle phase of the job",
    },
    "label": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 50,
        "DESCRIPTION": "Short textual label for the job",
        "EXAMPLES": ["LAMOST 2025 V883 Orionis Spectra Learning"],
    },
    "description": {
        "MIN_LENGTH": 1,
        "MAX_LENGTH": 255,
        "DESCRIPTION": "Extended textual description of the job",
        "EXAMPLES": ["New LAMOST 2025 V883 Orionis data set"],
    },
    "created_at": {
        "DESCRIPTION": "UTC datetime when the job was created",
        "EXAMPLES": ["2025-03-03T12:00:00Z"],
    },
    "started_at": {
        "DESCRIPTION": "UTC datetime when job execution started",
        "EXAMPLES": ["2025-03-03T12:25:00Z"],
    },
    "ended_at": {
        "DESCRIPTION": "UTC datetime when job execution ended",
        "EXAMPLES": ["2023-03-03T12:28:00Z"],
    },
    "execution_duration": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Total execution time of the job in seconds",
        "EXAMPLES": [180],
    },
}

list_resources = {
    "total": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Total number of jobs in the system",
        "EXAMPLES": [123],
    },
    "offset": {
        "MIN_VALUE": 0,
        "DEFAULT_VALUE": 0,
        "DESCRIPTION": "Zero-based index of the first returned job",
        "EXAMPLES": [10],
    },
    "limit": {
        "MIN_VALUE": 0,
        "DEFAULT_VALUE": 10,
        "DESCRIPTION": "Maximum number of jobs returned",
        "EXAMPLES": [1],
    },
    "jobs": {
        "DESCRIPTION": "List of summarized job records",
    },
}
