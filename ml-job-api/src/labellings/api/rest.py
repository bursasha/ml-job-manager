from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    status,
)
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv

from src.labellings.api.dependencies import get_service_using_postgres
from src.labellings.dto import (
    LabellingEditDTO,
    LabellingInitializeDTO,
)
from src.labellings.errors import (
    LabellingAbsentJobError,
    LabellingInvalidBatchError,
    LabellingNotExistError,
)
from src.labellings.resources import rest_resources
from src.labellings.serializers import (
    LabellingListSerializer,
    LabellingReadSerializer,
)
from src.labellings.service import LabellingService


rest_router = APIRouter(
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": rest_resources["HTTP_422"]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": rest_resources["HTTP_500"]},
    },
)


@cbv(rest_router)
class LabellingRESTRouter:
    """
    RESTful API router for labellings data operations.
    """

    service: LabellingService = Depends(get_service_using_postgres)

    @rest_router.post(
        path="/",
        tags=["Labellings: CRUD"],
        response_class=JSONResponse,
        response_model=LabellingReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_201_CREATED: {"description": rest_resources["initialize"]["HTTP_201"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["initialize"]["HTTP_404"]},
        },
        summary=rest_resources["initialize"]["SUMMARY"],
        description=rest_resources["initialize"]["DESCRIPTION"],
    )
    async def initialize_labelling(
        self,
        dto: LabellingInitializeDTO = Body(title="Labelling initialization payload"),
    ) -> LabellingReadSerializer:
        try:
            return await self.service.initialize_labelling(dto)

        except LabellingAbsentJobError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.get(
        path="/{labelling_id}",
        tags=["Labellings: CRUD"],
        response_class=JSONResponse,
        response_model=LabellingReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["retrieve"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["retrieve"]["HTTP_404"]},
        },
        summary=rest_resources["retrieve"]["SUMMARY"],
        description=rest_resources["retrieve"]["DESCRIPTION"],
    )
    async def retrieve_labelling(
        self,
        labelling_id: UUID = Path(title="Labelling ID"),
    ) -> LabellingReadSerializer:
        try:
            return await self.service.retrieve_labelling_by_labelling_id(labelling_id)

        except LabellingNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.patch(
        path="/{labelling_id}",
        tags=["Labellings: CRUD"],
        response_class=JSONResponse,
        response_model=LabellingReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["edit"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["edit"]["HTTP_404"]},
        },
        summary=rest_resources["edit"]["SUMMARY"],
        description=rest_resources["edit"]["DESCRIPTION"],
    )
    async def edit_labelling(
        self,
        labelling_id: UUID = Path(title="Labelling ID"),
        dto: LabellingEditDTO = Body(title="Labelling edition payload"),
    ) -> LabellingReadSerializer:
        try:
            return await self.service.edit_labelling_by_labelling_id(labelling_id, dto)

        except LabellingNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.post(
        path="/batch/",
        tags=["Labellings: Batch"],
        response_class=JSONResponse,
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_204_NO_CONTENT: {"description": rest_resources["initialize_batch"]["HTTP_204"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["initialize_batch"]["HTTP_404"]},
        },
        summary=rest_resources["initialize_batch"]["SUMMARY"],
        description=rest_resources["initialize_batch"]["DESCRIPTION"],
    )
    async def initialize_labellings_batch(
        self,
        batch: list[LabellingInitializeDTO] = Body(title="Labelling initialization batch payload"),
    ) -> None:
        try:
            await self.service.initialize_labellings_batch(batch)

        except LabellingAbsentJobError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.patch(
        path="/batch/",
        tags=["Labellings: Batch"],
        response_class=JSONResponse,
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_204_NO_CONTENT: {"description": rest_resources["edit_batch"]["HTTP_204"]},
            status.HTTP_400_BAD_REQUEST: {"description": rest_resources["edit_batch"]["HTTP_400"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["edit_batch"]["HTTP_404"]},
        },
        summary=rest_resources["edit_batch"]["SUMMARY"],
        description=rest_resources["edit_batch"]["DESCRIPTION"],
    )
    async def edit_labellings_batch(
        self,
        labelling_ids: list[UUID] = Body(title="Labelling IDs"),
        batch: list[LabellingEditDTO] = Body(title="Labelling edition batch payload"),
    ) -> None:
        try:
            await self.service.edit_labellings_batch_by_labelling_ids(labelling_ids, batch)

        except LabellingInvalidBatchError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        except LabellingNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.get(
        path="/",
        tags=["Labellings: List"],
        response_class=JSONResponse,
        response_model=LabellingListSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["list"]["HTTP_200"]},
        },
        summary=rest_resources["list"]["SUMMARY"],
        description=rest_resources["list"]["DESCRIPTION"],
    )
    async def list_labellings(
        self,
        job_id: UUID = Query(title="Job ID"),
    ) -> LabellingListSerializer:
        return await self.service.list_labellings_by_job_id(job_id)
