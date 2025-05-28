"""
Centralized API metadata definitions.
"""

rest_resources = {
    "HTTP_422": "Unprocessable Entity — one or more input parameters failed validation",
    "HTTP_500": "Internal Server Error — an unexpected error occurred during processing",
    "initialize": {
        "HTTP_201": "Job initialized successfully",
        "SUMMARY": "Initialize a new job",
        "DESCRIPTION": (
            "Accepts a JSON payload with job type, label and optional description; "
            "initializes a new job record with a generated `job_id` and directory path. "
            "Possible errors: 422 for invalid inputs, 500 for persistence failures."
        ),
    },
    "retrieve": {
        "HTTP_200": "Job retrieved successfully",
        "HTTP_404": "Requested job not found",
        "SUMMARY": "Retrieve a job",
        "DESCRIPTION": (
            "Retrieves full details of the job identified by path parameter `job_id`. "
            "Possible errors: 404 if not found, 422 for invalid `job_id`, 500 for retrieval failures."
        ),
    },
    "edit": {
        "HTTP_200": "Job edited successfully",
        "HTTP_404": "Requested job not found",
        "SUMMARY": "Edit a job",
        "DESCRIPTION": (
            "Accepts a JSON payload with edited job attributes (e.g. description) and applies "
            "changes to the specified job. Possible errors: 404 if not found, 422 for invalid inputs, "
            "500 for update failures."
        ),
    },
    "remove": {
        "HTTP_204": "Job removed successfully",
        "HTTP_404": "Requested job not found",
        "HTTP_409": "Job cannot be removed in its current phase",
        "SUMMARY": "Remove a job",
        "DESCRIPTION": (
            "Removes the job identified by `job_id` if it is in a removable phase: "
            "PENDING, COMPLETED, ERROR or ABORTED. Also cascades removing of all associated "
            "labelling records from the system. Possible errors: 404 if not found, "
            "409 if phase conflict, 422 for invalid `job_id`, 500 for removing failures."
        ),
    },
    "process": {
        "HTTP_202": "Job process action accepted",
        "HTTP_404": "Requested job not found",
        "HTTP_409": "Invalid phase for process action",
        "SUMMARY": "Process a job",
        "DESCRIPTION": (
            "Runs or aborts processing of the job identified by `job_id` and `process_action` path parameter,"
            "if it is in appropriate phase: PENDING for run action, PROCESSING for abort action. "
            "Possible errors: 404 if not found, 409 if the job is in an invalid phase for the action, "
            "422 for invalid inputs, 500 for queueing failures."
        ),
    },
    "end": {
        "HTTP_200": "Job end action applied",
        "HTTP_404": "Requested job not found",
        "HTTP_409": "Invalid phase for end action",
        "SUMMARY": "End a job",
        "DESCRIPTION": (
            "Marks the job as completed or errored based on `end_action` and provided processing metrics,"
            "if it is in appropriate phase: PROCESSING for complete action, PROCESSING for error action. "
            "Possible errors: 404 if not found, 409 if the job is in an invalid phase, "
            "422 for invalid inputs, 500 for update failures."
        ),
    },
    "list": {
        "HTTP_200": "Jobs list retrieved successfully",
        "SUMMARY": "List jobs",
        "DESCRIPTION": (
            "Retrieves a list of job summaries based on `offset` and `limit` query parameters. "
            "Possible errors: 422 for invalid pagination parameters, 500 for retrieval failures."
        ),
    },
}
