from fastapi import APIRouter

from src.jobs.api.rest import rest_router


jobs_api_router = APIRouter(prefix="/jobs")

jobs_api_router.include_router(rest_router)


__all__ = [
    "jobs_api_router",
]
