from uuid import UUID

from httpx import Client

from src.common.serializers import JobEndSerializer
from src.common.types import JobEndActionType


class JobHttpxAPI:
    """
    HTTP client for interacting with the ML Job API endpoints.
    """

    def __init__(self, api_client: Client) -> None:
        """
        Initialize the JobHttpxAPI with a preconfigured HTTP client.

        Parameters:
            api_client (Client): An httpx Client instance set up with base URL and other settings.
        """

        self.api = api_client

    def end_job_by_job_id_and_job_end_action(
        self, job_id: UUID, job_end_action: JobEndActionType, serializer: JobEndSerializer
    ) -> None:
        """
        Send a request to mark a job as completed or errored.

        This method serializes the end-of-job metrics into JSON and POSTs them to the
        `/jobs/{job_id}/end/{job_end_action}` endpoint.

        Parameters:
            job_id (UUID): Unique identifier of the job to end.
            job_end_action (JobEndActionType): The action type, either COMPLETE or ERROR.
            serializer (JobEndSerializer): Serializer data model containing job execution metrics.
        """

        response = serializer.model_dump(mode="json")

        self.api.post(f"/jobs/{job_id}/end/{job_end_action}", json=response)
