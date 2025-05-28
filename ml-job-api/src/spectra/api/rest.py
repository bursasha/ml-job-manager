from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv

from src.spectra.api.dependencies import get_service_using_lfs
from src.spectra.errors import SpectrumNotExistError
from src.spectra.resources import (
    rest_resources,
    spectrum_resources,
)
from src.spectra.serializers import SpectrumReadSerializer
from src.spectra.service import SpectrumService


rest_router = APIRouter(
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": rest_resources["HTTP_422"]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": rest_resources["HTTP_500"]},
    },
)


@cbv(rest_router)
class SpectrumRESTRouter:
    """
    RESTful API router for spectral data operations.
    """

    service: SpectrumService = Depends(get_service_using_lfs)

    @rest_router.get(
        path="/{filename}",
        tags=["Spectra: CRUD"],
        response_class=JSONResponse,
        response_model=SpectrumReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["retrieve"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["retrieve"]["HTTP_404"]},
        },
        summary=rest_resources["retrieve"]["SUMMARY"],
        description=rest_resources["retrieve"]["DESCRIPTION"],
    )
    async def retrieve_spectrum(
        self,
        filename: str = Path(
            title="Name of the spectrum FITS file",
            min_length=spectrum_resources["filename"]["MIN_LENGTH"],
            max_length=spectrum_resources["filename"]["MAX_LENGTH"],
            pattern=spectrum_resources["filename"]["PATTERN"],
        ),
    ) -> SpectrumReadSerializer:
        try:
            return await self.service.retrieve_spectrum_by_filename(filename)

        except SpectrumNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
