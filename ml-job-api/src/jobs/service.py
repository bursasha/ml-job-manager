from uuid import UUID

from src.common.utils import (
    generate_uuid,
    get_current_utc_datetime,
    get_duration_in_seconds,
)
from src.jobs.dto import (
    JobCreateDTO,
    JobEditDTO,
    JobEndDTO,
    JobInitializeDTO,
    JobStartDTO,
    JobUpdateDTO,
)
from src.jobs.errors import JobPhaseConflictError
from src.jobs.params import JobListParams
from src.jobs.queue import JobQueue
from src.jobs.repository import JobRepository
from src.jobs.serializers import (
    JobListSerializer,
    JobReadSerializer,
    JobSummarizeSerializer,
)
from src.jobs.types import (
    EndActionType,
    PhaseType,
    ProcessActionType,
)


class JobService:
    """
    Business logic layer for managing ML job lifecycle and orchestration.
    """

    def __init__(self, repository: JobRepository, queue: JobQueue) -> None:
        """
        Initialize the job service with repository and queue implementations.

        Parameters:
            repository (JobRepository): Concrete repository for persisting job records.
            queue (JobQueue): Concrete queue for dispatching and aborting asynchronous jobs.
        """

        self.repository = repository
        self.queue = queue

    @staticmethod
    def _generate_job_id_and_dir_path(label: str) -> tuple[UUID, str]:
        """
        Generate a new UUID and normalized directory path for a job.

        Parameters:
            label (str): User-provided job label.

        Returns:
            tuple[UUID, str]: A new job UUID and the storage directory path.
        """

        job_id = generate_uuid()
        norm_label = label.lower().replace(" ", "_")
        dir_path = f"/JOBS/job_{norm_label}_{job_id}"

        return job_id, dir_path

    async def initialize_job(self, dto: JobInitializeDTO) -> JobReadSerializer:
        """
        Create and persist a new job record in the PENDING phase.

        Parameters:
            dto (JobInitializeDTO): Payload containing job type, label, and optional description.

        Returns:
            JobReadSerializer: Full job record.
        """

        job_id, dir_path = self._generate_job_id_and_dir_path(dto.label)
        created_at = get_current_utc_datetime()
        entity = await self.repository.create(
            JobCreateDTO(
                job_id=job_id,
                dir_path=dir_path,
                phase=PhaseType.PENDING,
                created_at=created_at,
                **dto.model_dump(),
            )
        )

        return JobReadSerializer(**entity.model_dump())

    async def retrieve_job_by_job_id(self, job_id: UUID) -> JobReadSerializer:
        """
        Retrieve the full details of an existing job.

        Parameters:
            job_id (UUID): Unique identifier of the job to fetch.

        Returns:
            JobReadSerializer: Full job details.
        """

        entity = await self.repository.get_by_job_id(job_id)

        return JobReadSerializer(**entity.model_dump())

    async def edit_job_by_job_id(self, job_id: UUID, dto: JobEditDTO) -> JobReadSerializer:
        """
        Edit mutable attributes of an existing job record.

        Parameters:
            job_id (UUID): Unique identifier of the job to edit.
            dto (JobEditDTO): Payload containing updated job fields.

        Returns:
            JobReadSerializer: Updated job record.
        """

        entity = await self.repository.update_by_job_id(job_id, JobUpdateDTO(**dto.model_dump()))

        return JobReadSerializer(**entity.model_dump())

    async def remove_job_by_job_id(self, job_id: UUID) -> None:
        """
        Delete a job record if it is in a removable phase.

        Allowed phases: PENDING, COMPLETED, ERROR, ABORTED.

        Parameters:
            job_id (UUID): Unique identifier of the job to delete.

        Raises:
            JobPhaseConflictError: Conflict if current phase disallows deletion.
        """

        entity = await self.repository.get_by_job_id(job_id)
        allowed_operation_phases = {
            PhaseType.PENDING,
            PhaseType.COMPLETED,
            PhaseType.ERROR,
            PhaseType.ABORTED,
        }

        if not (entity.phase in allowed_operation_phases):
            raise JobPhaseConflictError(f"Cannot remove job with ID={entity.job_id} in current phase={entity.phase}.")

        await self.repository.delete_by_job_id(entity.job_id)

    async def manage_job_by_job_id_and_process_action(
        self, job_id: UUID, process_action: ProcessActionType
    ) -> JobReadSerializer:
        """
        Run or abort asynchronous processing of a job.

        RUN action allowed only in PENDING phase.
        ABORT action allowed only in PROCESSING phase.

        Parameters:
            job_id (UUID): Unique identifier of the job.
            process_action (ProcessActionType): RUN or ABORT.

        Returns:
            JobReadSerializer: Updated job record after enqueue or abort.

        Raises:
            JobPhaseConflictError: Conflict if action invalid for current phase.
        """

        entity = await self.repository.get_by_job_id(job_id)
        allowed_operation_phases = {
            ProcessActionType.RUN: {
                PhaseType.PENDING,
            },
            ProcessActionType.ABORT: {
                PhaseType.PROCESSING,
            },
        }

        for allowed_operation_action in allowed_operation_phases.keys():
            if process_action == allowed_operation_action and not (
                entity.phase in allowed_operation_phases[allowed_operation_action]
            ):
                raise JobPhaseConflictError(
                    f"Cannot process process action={process_action} on job with ID={entity.job_id} "
                    f"in current phase={entity.phase}."
                )

        if process_action == ProcessActionType.RUN:
            self.queue.run_by_job_id_and_job_type(entity.job_id, entity.type, JobStartDTO(dir_path=entity.dir_path))
            entity = await self.repository.update_by_job_id(entity.job_id, JobUpdateDTO(phase=PhaseType.PROCESSING))

        elif process_action == ProcessActionType.ABORT:
            self.queue.abort_by_job_id(entity.job_id)
            entity = await self.repository.update_by_job_id(entity.job_id, JobUpdateDTO(phase=PhaseType.ABORTED))

        return JobReadSerializer(**entity.model_dump())

    async def manage_job_by_job_id_and_end_action(
        self, job_id: UUID, end_action: EndActionType, dto: JobEndDTO
    ) -> JobReadSerializer:
        """
        Finalize a processing job as completed or errored.

        COMPLETE and ERROR actions allowed only in PROCESSING phase.

        Parameters:
            job_id (UUID): Unique identifier of the job.
            end_action (EndActionType): COMPLETE or ERROR.
            dto (JobEndDTO): Payload with the execution metrics.

        Returns:
            JobReadSerializer: Updated job record with final phase and metrics.

        Raises:
            JobPhaseConflictError: 409 Conflict if action invalid for current phase
        """

        entity = await self.repository.get_by_job_id(job_id)
        allowed_operation_phases = {
            EndActionType.COMPLETE: {
                PhaseType.PROCESSING,
            },
            EndActionType.ERROR: {
                PhaseType.PROCESSING,
            },
        }

        for allowed_operation_action in allowed_operation_phases.keys():
            if end_action == allowed_operation_action and not (
                entity.phase in allowed_operation_phases[allowed_operation_action]
            ):
                raise JobPhaseConflictError(
                    f"Cannot process end action={end_action} on job with ID={entity.job_id} "
                    f"in current phase={entity.phase}."
                )

        execution_duration = get_duration_in_seconds(dto.started_at, dto.ended_at)

        if end_action == EndActionType.COMPLETE:
            entity = await self.repository.update_by_job_id(
                entity.job_id,
                JobUpdateDTO(
                    phase=PhaseType.COMPLETED,
                    started_at=dto.started_at,
                    ended_at=dto.ended_at,
                    execution_duration=execution_duration,
                ),
            )

        elif end_action == EndActionType.ERROR:
            entity = await self.repository.update_by_job_id(
                entity.job_id,
                JobUpdateDTO(
                    phase=PhaseType.ERROR,
                    started_at=dto.started_at,
                    ended_at=dto.ended_at,
                    execution_duration=execution_duration,
                ),
            )

        return JobReadSerializer(**entity.model_dump())

    async def list_jobs(self, params: JobListParams) -> JobListSerializer:
        """
        Retrieve a paginated list of job summaries.

        Parameters:
            params (JobListParams): Pagination parameters.

        Returns:
            JobListSerializer: Total count, offset, limit, and list of JobSummarizeSerializer.
        """

        total = await self.repository.total()
        entities = await self.repository.list_by_offset_and_limit(params.offset, params.limit)
        serializers = [JobSummarizeSerializer(**entity.model_dump()) for entity in entities]

        return JobListSerializer(total=total, offset=params.offset, limit=params.limit, jobs=serializers)
