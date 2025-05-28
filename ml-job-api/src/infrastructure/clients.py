from celery import Celery

from src.settings.clients import celery_settings


#


# Create the global Celery client
celery_client = Celery()

# Load broker URL, default queue, and retry settings from CelerySettings
celery_client.config_from_object(
    obj=celery_settings,
    silent=False,
    force=True,
)
