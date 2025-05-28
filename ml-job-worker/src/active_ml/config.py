from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

class ActiveLearningConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    iteration: int = Field(
        ...,
        description="Job's iteration number",
        examples=[0], 
    )

    classes: list[str] = Field(
        ...,
        description="List of spectrum classification classes",
        examples=[["other", "single peak", "double peak"]], 
    )

    candidate_classes: list[str] = Field(
        ...,
        description="List of candidate classes",
        examples=[["single peak", "double peak"]], 
    )

    training_data_path: str = Field(
        "",
        description="Path to file containing training data.",
        examples=["/Data/training_data.h5"], 
    )

    training_data_to_add_path: str = Field(
        "",
        description="Path to file containing additional training data.",
        examples=["/Data/training_data_to_add.h5"], 
    )

    oracle_data_to_add_path: str = Field(
        "",
        description="Path to file containing labels for additinional training data.",
        examples=["/Data/oracle_data_to_add.json"], 
    )

    pool_data_path: str = Field(
        ...,
        description="Path to file containing pool data.",
        examples=["/Data/pool_data.h5"], 
    )

    oracle_batch_size: int = Field(
        100,
        description="Number of spectra to query the oracle.",
        examples=[100], 
    )

    perf_est_batch_size: int = Field(
        10,
        description="Number of spectra for performance estimation.",
        examples=[10], 
    )

    show_candidates: bool = Field(
        False,
        description="If true, saves spectra, which was predicted as candidate.",
        examples=[False],
    )

    save_model: bool = Field(
        False,
        description="If true, saves the model.",
        examples=[False],
    )

    min_delta_train: float = Field(
        10e-4,
        description="Min delta for model training.",
        examples=[10e-4],
    )

    patience_train: float = Field(
        10,
        description="Patience for model training",
        examples=[10],
    )

    batch_size_train: int = Field(
        64,
        description="Batch size for model training",
        examples=[64],
    )

    epochs_train: int = Field(
        1000,
        description="Epochs for model training",
        examples=[1000],
    )

    batch_size_predict: int = Field(
        2**14,
        description="Batch size for model prediction",
        examples=[16384],
    )

    perf_est_list_path: str = Field(
        "",
        description="Path to file containing performances from previous iteration.",
        examples=["/job_lamost_123/perf_est_list.json"],
    )

    result_dir_path: str | None = Field(
        None,
        description="Path to the result directory of current job.",
        examples=["/job_lamost_123"],
    )

    job_dir: str | None = Field(
        None,
        description="Job's directory name.",
        examples=["/JOBS/job_lamost_123"],
    )
