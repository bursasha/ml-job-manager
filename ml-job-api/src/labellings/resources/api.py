"""
Centralized API metadata definitions.
"""

rest_resources = {
    "HTTP_422": "Unprocessable Entity — one or more input parameters failed validation",
    "HTTP_500": "Internal Server Error — an unexpected error occurred during processing",
    "initialize": {
        "HTTP_201": "Labelling initialized successfully",
        "HTTP_404": "Associated job not found",
        "SUMMARY": "Initialize a new labelling",
        "DESCRIPTION": (
            "Accepts a JSON payload with job identifier, spectrum filename, spectrum set, sequence iteration, "
            "and optional model prediction, user label/comment; generates a `labelling_id` and persists the record. "
            "Possible errors: 404 if associated job not found, 422 for invalid inputs, 500 for persistence failures."
        ),
    },
    "retrieve": {
        "HTTP_200": "Labelling retrieved successfully",
        "HTTP_404": "Requested labelling not found",
        "SUMMARY": "Retrieve a labelling",
        "DESCRIPTION": (
            "Retrieves the labelling record identified by path parameter `labelling_id`. "
            "Possible errors: 404 if not found, 422 for invalid `labelling_id`, 500 for retrieval failures."
        ),
    },
    "edit": {
        "HTTP_200": "Labelling updated successfully",
        "HTTP_404": "Requested labelling not found",
        "SUMMARY": "Edit a labelling",
        "DESCRIPTION": (
            "Accepts a JSON payload with edited user label and/or comment; applies changes to the specified labelling. "
            "Possible errors: 404 if not found, 422 for invalid inputs, 500 for edition failures."
        ),
    },
    "initialize_batch": {
        "HTTP_204": "Batch of labellings initialized successfully",
        "HTTP_404": "One or more associated jobs in the batch do not exist",
        "SUMMARY": "Initialize a new batch of labellings",
        "DESCRIPTION": (
            "Accepts an array of labelling payloads; generates IDs and persists multiple records in one request. "
            "Possible errors: 404 if any associated job ID is missing, 422 for invalid inputs, "
            "500 for persistence failures."
        ),
    },
    "edit_batch": {
        "HTTP_204": "Batch of labellings updated successfully",
        "HTTP_400": "Mismatch between provided IDs and edition payloads",
        "HTTP_404": "One or more labellings in the batch do not exist",
        "SUMMARY": "Edit a batch of labellings",
        "DESCRIPTION": (
            "Accepts parallel arrays of labelling IDs and edition payloads; applies label/comment editions in bulk. "
            "Possible errors: 400 for IDs/payloads length mismatch, 404 if any ID is missing, "
            "422 for invalid inputs, 500 for edition failures."
        ),
    },
    "list": {
        "HTTP_200": "Labellings list retrieved successfully",
        "SUMMARY": "List labellings by job ID",
        "DESCRIPTION": (
            "Retrieves all labelling records associated with query parameter `job_id`. "
            "Possible errors: 422 for invalid `job_id`, 500 for retrieval failures."
        ),
    },
}
