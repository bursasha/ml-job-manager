from fastapi import (
    APIRouter,
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from src.files.api import files_api_router
from src.jobs.api import jobs_api_router
from src.labellings.api import labellings_api_router
from src.settings.app import app_settings
from src.spectra.api import spectra_api_router


# Create the main FastAPI application instance, using settings from app_settings
app = FastAPI(
    title=app_settings.title,
    description=app_settings.description,
    version=app_settings.version,
    debug=app_settings.debug,
)

# Enable CORS for all origins, methods, headers, and credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Mount all sub-routers under the '/api' prefix
api_router = APIRouter(prefix="/api")

api_router.include_router(files_api_router)
api_router.include_router(jobs_api_router)
api_router.include_router(labellings_api_router)
api_router.include_router(spectra_api_router)

# Include the combined API router into the application
app.include_router(api_router)
