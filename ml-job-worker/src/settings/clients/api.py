from pydantic import (
    Field,
    HttpUrl,
    field_validator,
)
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """
    Configuration settings for the ML Job API client integration.
    All values may be loaded from environment variables.
    """

    api_url: str = Field(
        ...,
        description="Base HTTP URL of the ML Job API microservice for sending requests",
    )

    api_connection_timeout: int = Field(
        ...,
        description="Maximum seconds to wait when establishing or reusing an HTTP connection to the API",
    )

    @field_validator("api_url")
    def build_api_url(cls, api_url: str) -> str:
        http_url = HttpUrl(api_url)

        return str(http_url)


api_settings = APISettings()
