from uuid import UUID

from celery import Celery

from src.jobs.dto import JobStartDTO
from src.jobs.queue import JobQueue
from src.jobs.types import JobType


class JobCeleryQueue(JobQueue):
    """
    Celery-backed implementation of JobQueue.
    """

    def __init__(self, celery_client: Celery) -> None:
        """
        Initialize with a configured Celery client.

        Parameters:
            celery_client (Celery): The Celery application instance used to send and control jobs.
        """

        self.queue = celery_client

    def run_by_job_id_and_job_type(self, job_id: UUID, job_type: JobType, dto: JobStartDTO) -> None:
        """
        Enqueue a new Celery task for the given job.

        This sends a Celery task whose `task_id` is set to the job_id string and whose
        name matches the JobType enum. The DTO is serialized into kwargs.

        Parameters:
            job_id (UUID): The unique identifier for this job; becomes the Celery task ID.
            job_type (JobType): The registered Celery task name indicating which worker handler to invoke.
            dto (JobStartDTO): DTO containing job initialization parameters; will be passed as keyword arguments.
        """

        self.queue.send_task(task_id=str(job_id), name=job_type, kwargs={"dto": dto.model_dump()})

    def abort_by_job_id(self, job_id: UUID) -> None:
        """
        Revoke a running or queued Celery task.

        This sends a revoke command with terminate=True, causing a SIGTERM to be
        delivered to the worker process if it is active.

        Parameters:
            job_id (UUID): The unique identifier of the job/Celery task to abort.
        """

        self.queue.control.revoke(task_id=str(job_id), terminate=True)
