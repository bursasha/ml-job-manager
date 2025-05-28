"""
Centralized entity metadata definitions.
"""

file_resources = {
    "filename": {
        "MIN_LENGTH": 1,
        "DESCRIPTION": "Name of the file, including its extension",
        "EXAMPLES": ["spec-56207-M31011N44B2_sp01-006.fits"],
    },
    "parent_dir_path": {
        "MIN_LENGTH": 1,
        "PATTERN": r"^(?:[\\/](?:[^\\/]+(?:[\\/][^\\/]+)*)?)$",
        "DESCRIPTION": "Path to the parent directory, containing the file",
        "EXAMPLES": ["/SPECTRA/M31011N44B2"],
    },
    "size": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Size of the file in bytes",
        "EXAMPLES": [500],
    },
    "modified_at": {
        "DESCRIPTION": "UTC datetime when the file was last modified",
        "EXAMPLES": ["2025-04-04T12:00:00Z"],
    },
}

directory_resources = {
    "dirname": {
        "MIN_LENGTH": 1,
        "DESCRIPTION": "Name of the directory",
        "EXAMPLES": ["job_lamost_2025_spectra_learning_3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    },
    "parent_dir_path": {
        "MIN_LENGTH": file_resources["parent_dir_path"]["MIN_LENGTH"],
        "PATTERN": file_resources["parent_dir_path"]["PATTERN"],
        "DESCRIPTION": "Path to the parent directory, containing the directory",
        "EXAMPLES": ["/JOBS"],
    },
}

list_resources = {
    "parent_dir_path": {
        "MIN_LENGTH": file_resources["parent_dir_path"]["MIN_LENGTH"],
        "PATTERN": file_resources["parent_dir_path"]["PATTERN"],
        "DEFAULT_VALUE": "/",
        "DESCRIPTION": "Path to the parent directory whose contents will be listed",
        "EXAMPLES": ["/"],
    },
    "total": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Total number of files and directories in the parent directory",
        "EXAMPLES": [2],
    },
    "file_count": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Number of files in the specified directory",
        "EXAMPLES": [1],
    },
    "directory_count": {
        "MIN_VALUE": 0,
        "DESCRIPTION": "Number of directories in the specified directory",
        "EXAMPLES": [1],
    },
    "files": {
        "DESCRIPTION": "List of file summaries in the directory",
    },
    "directories": {
        "DESCRIPTION": "List of directory summaries in the directory",
    },
}
