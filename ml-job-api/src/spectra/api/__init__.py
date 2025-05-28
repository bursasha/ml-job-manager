from fastapi import APIRouter

from src.spectra.api.rest import rest_router


spectra_api_router = APIRouter(prefix="/spectra")

spectra_api_router.include_router(rest_router)


__all__ = [
    "spectra_api_router",
]
