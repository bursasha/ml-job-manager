from pydantic import (
    BaseModel,
    Field,
)


class JobStartDTO(BaseModel):
    """
    Data Transfer Object model used to initiate the asynchronous execution of a Job.
    """

    dir_path: str = Field(
        ...,
        min_length=1,
        pattern=r"^(?:[\\/](?:[^\\/]+(?:[\\/][^\\/]+)*)?)$",
        description="Storage directory path where job outputs/results are stored",
        examples=["/JOBS/job_lamost_2025_v883_orionis_spectra_learning_3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )
