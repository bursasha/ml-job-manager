"""
Centralized API metadata definitions.
"""

rest_resources = {
    "HTTP_422": "Unprocessable Entity — one or more input parameters failed validation",
    "HTTP_500": "Internal Server Error — an unexpected error occurred during processing",
    "retrieve": {
        "HTTP_200": "Spectrum retrieved successfully",
        "HTTP_404": "Requested spectrum not found",
        "SUMMARY": "Retrieve a spectrum",
        "DESCRIPTION": (
            "Retrieves and parses the FITS spectrum identified by path parameter `filename`, "
            "and returns its header metadata and data arrays. "
            "Possible errors: 404 if the spectrum is missing, 422 for invalid inputs, "
            "500 for backend or parsing failures."
        ),
    },
}
