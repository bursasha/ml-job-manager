from httpx import Client

from src.settings.clients import api_settings


#


# HTTP client for sending requests to the ML Job API microservice
api_client = Client(
    base_url=api_settings.api_url,
    timeout=api_settings.api_connection_timeout,
)
