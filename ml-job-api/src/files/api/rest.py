from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import (
    JSONResponse,
    StreamingResponse,
)
from fastapi_restful.cbv import cbv

from src.files.api.dependencies import get_service_using_lfs
from src.files.errors import (
    DirectoryAlreadyExistError,
    DirectoryNotExistError,
    FileNotExistError,
)
from src.files.params import (
    EntryListParams,
    EntryLocateParams,
)
from src.files.resources import rest_resources
from src.files.serializers import (
    DirectoryReadSerializer,
    EntryListSerializer,
    FileReadSerializer,
)
from src.files.service import FileService


rest_router = APIRouter(
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": rest_resources["HTTP_422"]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": rest_resources["HTTP_500"]},
    },
)


@cbv(rest_router)
class FileRESTRouter:
    """
    RESTful API router for files and directories data operations.
    """

    service: FileService = Depends(get_service_using_lfs)

    @rest_router.post(
        path="/{filename}/upload",
        tags=["Files: Load"],
        response_class=JSONResponse,
        response_model=FileReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_201_CREATED: {"description": rest_resources["upload"]["HTTP_201"]},
        },
        summary=rest_resources["upload"]["SUMMARY"],
        description=rest_resources["upload"]["DESCRIPTION"],
    )
    async def upload_file(
        self,
        filename: str = Path(title="Name of the file"),
        params: EntryLocateParams = Query(title="Location parameters of the file"),
        file: UploadFile = File(title="File to upload"),
    ) -> FileReadSerializer:
        return await self.service.upload_file_by_filename(filename, params, file)

    @rest_router.get(
        path="/{filename}/download",
        tags=["Files: Load"],
        response_class=StreamingResponse,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["download"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["download"]["HTTP_404"]},
        },
        summary=rest_resources["download"]["SUMMARY"],
        description=rest_resources["download"]["DESCRIPTION"],
    )
    async def download_file(
        self,
        filename: str = Path(title="Name of the file"),
        params: EntryLocateParams = Query(title="Location parameters of the file"),
    ) -> StreamingResponse:
        try:
            return StreamingResponse(
                await self.service.download_file_by_filename(filename, params),
                headers={"Content-Disposition": f'attachment; filename="{filename}"'},
                media_type="application/octet-stream",
            )

        except FileNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.delete(
        path="/{filename}",
        tags=["Files: CRUD"],
        response_class=JSONResponse,
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_204_NO_CONTENT: {"description": rest_resources["remove"]["HTTP_204"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["remove"]["HTTP_404"]},
        },
        summary=rest_resources["remove"]["SUMMARY"],
        description=rest_resources["remove"]["DESCRIPTION"],
    )
    async def remove_file(
        self,
        filename: str = Path(title="Name of the file"),
        params: EntryLocateParams = Query(title="Location parameters of the file"),
    ) -> None:
        try:
            await self.service.remove_file_by_filename(filename, params)

        except FileNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.post(
        path="/directories/{dirname}",
        tags=["Directories: CRUD"],
        response_class=JSONResponse,
        response_model=DirectoryReadSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_201_CREATED: {"description": rest_resources["initialize_directory"]["HTTP_201"]},
            status.HTTP_409_CONFLICT: {"description": rest_resources["initialize_directory"]["HTTP_409"]},
        },
        summary=rest_resources["initialize_directory"]["SUMMARY"],
        description=rest_resources["initialize_directory"]["DESCRIPTION"],
    )
    async def initialize_directory(
        self,
        dirname: str = Path(title="Name of the directory"),
        params: EntryLocateParams = Query(title="Location parameters of the directory"),
    ) -> DirectoryReadSerializer:
        try:
            return await self.service.initialize_directory_by_dirname(dirname, params)

        except DirectoryAlreadyExistError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    @rest_router.delete(
        path="/directories/{dirname}",
        tags=["Directories: CRUD"],
        response_class=JSONResponse,
        response_model=None,
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_204_NO_CONTENT: {"description": rest_resources["remove_directory"]["HTTP_204"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["remove_directory"]["HTTP_404"]},
        },
        summary=rest_resources["remove_directory"]["SUMMARY"],
        description=rest_resources["remove_directory"]["DESCRIPTION"],
    )
    async def remove_directory(
        self,
        dirname: str = Path(title="Name of the directory"),
        params: EntryLocateParams = Query(title="Location parameters of the directory"),
    ) -> None:
        try:
            await self.service.remove_directory_by_dirname(dirname, params)

        except DirectoryNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    @rest_router.get(
        path="/",
        tags=["Files: List"],
        response_class=JSONResponse,
        response_model=EntryListSerializer,
        response_model_exclude_none=True,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": rest_resources["list"]["HTTP_200"]},
            status.HTTP_404_NOT_FOUND: {"description": rest_resources["list"]["HTTP_404"]},
        },
        summary=rest_resources["list"]["SUMMARY"],
        description=rest_resources["list"]["DESCRIPTION"],
    )
    async def list_entries(
        self,
        params: EntryListParams = Query(title="Location parameters of files and directories"),
    ) -> EntryListSerializer:
        try:
            return await self.service.list_entries(params)

        except DirectoryNotExistError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
