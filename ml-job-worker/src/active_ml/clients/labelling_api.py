from httpx import Client

from src.active_ml.serializers import LabellingInitializeSerializer


class LabellingHttpxAPI:
    """
    HTTP client for interacting with the Labellings API of the ML Job service.
    """

    def __init__(self, api_client: Client) -> None:
        """
        Initialize the LabellingHttpxAPI with a configured HTTP client.

        Parameters:
            api_client (Client): An `httpx.Client` instance with base_url and other settings.
        """

        self.api = api_client

    def initialize_labellings_batch(self, batch: list[LabellingInitializeSerializer]) -> None:
        """
        Send a batch initialization request for multiple labellings.

        Serializes each `LabellingInitializeSerializer` to JSON and posts to the `/labellings/batch/` endpoint
        in a single array payload.

        Parameters:
            batch (list[LabellingInitializeSerializer]):
                List of serializers for initializing new labellings after Active ML Job workflow.
        """

        response = [serializer.model_dump(mode="json") for serializer in batch]

        self.api.post(f"/labellings/batch/", json=response)
