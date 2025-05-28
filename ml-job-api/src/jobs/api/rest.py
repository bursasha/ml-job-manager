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

from src.jobs.api.dependencies import get_service_using_postgres_and_celery
from src.jobs.dto import (
    JobEditDTO,
    JobEndDTO,
    JobInitializeDTO,
)
from src.jobs.errors import (
    JobNotExistError,
    JobPhaseConflictError,
)
from src.jobs.params import JobListParams
from src.jobs.resources import rest_resources
from src.jobs.serializers import (
    JobListSerializer,
    JobReadSerializer,
)
from src.jobs.service import JobService
from src.jobs.types import (
    EndActionType,
    ProcessActionType,
)


rest_router = APIRouter(
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": rest_resources["HTTP_422"]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": rest_resources["HTTP_500"]},
    },
)


@cbv(rest_router)
class JobRESTRouter:
    """
    RESTful API router for jobs data operations and orchestrations.
    """

    service: JobService = Depends(get_service_using_postgres_and_celery)

    @rest_router.post(
        path="/",
        tags=["Jobs: CRUD"],
        response_class=JSONResponse,
        response_model=JobReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_201_CREATED: {"description": rest_resources["initialize"]["HTTP_201"]},
        },
        summary=rest_resources["initialize"]["SUMMARY"],
        description=rest_resources["initialize"]["DESCRIPTION"],
    )
    async def initialize_job(
        self,
        dto: JobInitializeDTO = Body(title="Job initialization payload"),
    ) -> JobReadSerializer:
        return await self.service.initialize_job(dto)

    @rest_router.get(
        path="/{job_id}",
        tags=["Jobs: CRUD"],
        response_class=JSONResponse,
        response_model=JobReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["retrieve"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["retrieve"]["HTTP_404"]},
        },
        summary=rest_resources["retrieve"]["SUMMARY"],
        description=rest_resources["retrieve"]["DESCRIPTION"],
    )
    async def retrieve_job(
        self,
        job_id: UUID = Path(title="Job ID"),
    ) -> JobReadSerializer:
        try:
            return await self.service.retrieve_job_by_job_id(job_id)

        except JobNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.patch(
        path="/{job_id}",
        tags=["Jobs: CRUD"],
        response_class=JSONResponse,
        response_model=JobReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["edit"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["edit"]["HTTP_404"]},
        },
        summary=rest_resources["edit"]["SUMMARY"],
        description=rest_resources["edit"]["DESCRIPTION"],
    )
    async def edit_job(
        self,
        job_id: UUID = Path(title="Job ID"),
        dto: JobEditDTO = Body(title="Job edition payload"),
    ) -> JobReadSerializer:
        try:
            return await self.service.edit_job_by_job_id(job_id, dto)

        except JobNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.delete(
        path="/{job_id}",
        tags=["Jobs: CRUD"],
        response_class=JSONResponse,
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_204_NO_CONTENT: {"description": rest_resources["remove"]["HTTP_204"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["remove"]["HTTP_404"]},
            status.HTTP_409_CONFLICT: {"description": rest_resources["remove"]["HTTP_409"]},
        },
        summary=rest_resources["remove"]["SUMMARY"],
        description=rest_resources["remove"]["DESCRIPTION"],
    )
    async def remove_job(
        self,
        job_id: UUID = Path(title="Job ID"),
    ) -> None:
        try:
            await self.service.remove_job_by_job_id(job_id)

        except JobNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        except JobPhaseConflictError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @rest_router.post(
        path="/{job_id}/process/{process_action}",
        tags=["Jobs: Action"],
        response_class=JSONResponse,
        response_model=JobReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_202_ACCEPTED,
        responses={
            status.HTTP_202_ACCEPTED: {"description": rest_resources["process"]["HTTP_202"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["process"]["HTTP_404"]},
            status.HTTP_409_CONFLICT: {"description": rest_resources["process"]["HTTP_409"]},
        },
        summary=rest_resources["process"]["SUMMARY"],
        description=rest_resources["process"]["DESCRIPTION"],
    )
    async def process_job(
        self,
        job_id: UUID = Path(title="Job ID"),
        process_action: ProcessActionType = Path(title="Process action"),
    ) -> JobReadSerializer:
        try:
            return await self.service.manage_job_by_job_id_and_process_action(job_id, process_action)

        except JobNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        except JobPhaseConflictError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @rest_router.post(
        path="/{job_id}/end/{end_action}",
        tags=["Jobs: Action"],
        response_class=JSONResponse,
        response_model=JobReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["end"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["end"]["HTTP_404"]},
            status.HTTP_409_CONFLICT: {"description": rest_resources["end"]["HTTP_409"]},
        },
        summary=rest_resources["end"]["SUMMARY"],
        description=rest_resources["end"]["DESCRIPTION"],
    )
    async def end_job(
        self,
        job_id: UUID = Path(title="Job ID"),
        end_action: EndActionType = Path(title="End action"),
        dto: JobEndDTO = Body(title="Job end payload"),
    ) -> JobReadSerializer:
        try:
            return await self.service.manage_job_by_job_id_and_end_action(job_id, end_action, dto)

        except JobNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        except JobPhaseConflictError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @rest_router.get(
        path="/",
        tags=["Jobs: List"],
        response_class=JSONResponse,
        response_model=JobListSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["list"]["HTTP_200"]},
        },
        summary=rest_resources["list"]["SUMMARY"],
        description=rest_resources["list"]["DESCRIPTION"],
    )
    async def list_jobs(
        self,
        params: JobListParams = Query(title="Job list parameters"),
    ) -> JobListSerializer:
        return await self.service.list_jobs(params)
