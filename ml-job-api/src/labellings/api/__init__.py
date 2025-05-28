from fastapi import APIRouter

from src.labellings.api.rest import rest_router


labellings_api_router = APIRouter(prefix="/labellings")

labellings_api_router.include_router(rest_router)


__all__ = [
    "labellings_api_router",
]
