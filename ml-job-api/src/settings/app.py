from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    Configuration settings for the ML Job API application.
    All values can be loaded from environment variables.
    """

    debug: bool = Field(
        ...,
        description="Enable debug mode with detailed logging and auto‑reload",
    )

    title: str = Field(
        "ML Job API",
        description="The title displayed in the OpenAPI documentation",
    )

    description: str = Field(
        "Asynchronous ML Job API Microservice",
        description="A brief summary of this microservice’s purpose",
    )

    version: str = Field(
        "0.1.0",
        description="The current version of the API",
    )


app_settings = AppSettings()
