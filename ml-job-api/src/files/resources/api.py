"""
Centralized API metadata definitions.
"""

rest_resources = {
    "HTTP_422": "Unprocessable Entity — one or more input parameters failed validation",
    "HTTP_500": "Internal Server Error — an unexpected error occurred during processing",
    "upload": {
        "HTTP_201": "File uploaded successfully",
        "SUMMARY": "Upload a new file",
        "DESCRIPTION": (
            "Accepts a multipart/form-data request and stores the file in the configured backend. "
            "Requires path parameter `filename` and location query parameters. "
            "Returns metadata of the stored file. Possible errors: 422 for invalid inputs, "
            "500 for storage failures."
        ),
    },
    "download": {
        "HTTP_200": "File download stream started",
        "HTTP_404": "Requested file not found",
        "SUMMARY": "Download a file",
        "DESCRIPTION": (
            "Streams the contents of a stored file back to the client. "
            "Requires path parameter `filename` and location query parameters. "
            "Possible errors: 404 if the file is missing, 422 for invalid inputs, "
            "500 for backend errors."
        ),
    },
    "remove": {
        "HTTP_204": "File removed successfully",
        "HTTP_404": "Requested file not found",
        "SUMMARY": "Remove a file",
        "DESCRIPTION": (
            "Removes a stored file identified by `filename` and location parameters. "
            "No content is returned on success. Possible errors: 404 if the file is missing, "
            "422 for invalid inputs, 500 for deletion failures."
        ),
    },
    "initialize_directory": {
        "HTTP_201": "Directory initialized successfully",
        "HTTP_409": "Requested directory already exists",
        "SUMMARY": "Initialize a new directory",
        "DESCRIPTION": (
            "Initializes a new directory in the storage backend. "
            "Requires path parameter `dirname` and location query parameters. "
            "Possible errors: 409 if the directory already exists, "
            "422 for invalid inputs, 500 for backend errors."
        ),
    },
    "remove_directory": {
        "HTTP_204": "Directory removed successfully",
        "HTTP_404": "Requested directory not found",
        "SUMMARY": "Remove a directory",
        "DESCRIPTION": (
            "Recursively removes a directory and its contents from storage. "
            "Requires path parameter `dirname` and location query parameters. "
            "Possible errors: 404 if the directory is missing, 422 for invalid inputs, "
            "500 for deletion failures."
        ),
    },
    "list": {
        "HTTP_200": "File and directory list retrieved successfully",
        "HTTP_404": "Requested directory not found",
        "SUMMARY": "List directory contents",
        "DESCRIPTION": (
            "Retrieves summaries of all files and subdirectories under a given storage location. "
            "Requires location query parameters. Possible errors: 404 if the directory is missing, "
            "422 for invalid inputs, 500 for listing failures."
        ),
    },
}
