from fastapi import APIRouter

from src.files.api.rest import rest_router


files_api_router = APIRouter(prefix="/files")

files_api_router.include_router(rest_router)


__all__ = [
    "files_api_router",
]
