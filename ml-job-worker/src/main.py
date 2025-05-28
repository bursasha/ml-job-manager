from celery import Celery

from src.settings.app import app_settings


# Create the main Celery worker application instance
app = Celery()

# Include task modules so Celery can discover and register tasks
app.conf.include = [
    "src.active_ml",
    "src.data_preprocessing",
]

# Load Celery configuration directly from the Pydantic-based settings object
app.config_from_object(
    obj=app_settings,
    silent=False,  # Raise errors if config keys are missing
    force=True,    # Override any existing config values
)
