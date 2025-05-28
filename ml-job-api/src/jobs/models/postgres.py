from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.common.models import BasePostgresModel
from src.jobs.resources import job_resources
from src.jobs.types import (
    JobType,
    PhaseType,
)


class JobPostgresModel(BasePostgresModel):
    """
    SQLAlchemy ORM model for the `jobs` table, representing ML job records.
    """

    __tablename__ = "jobs"

    repr_columns = (
        "job_id",
        "type",
        "label",
        "created_at",
    )

    job_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        comment="Job ID",
    )

    dir_path: Mapped[str] = mapped_column(
        String(job_resources["dir_path"]["MAX_LENGTH"]),
        nullable=False,
        comment="Job directory path",
    )

    type: Mapped[JobType] = mapped_column(
        Enum(JobType),
        nullable=False,
        comment="Job type",
    )

    phase: Mapped[PhaseType] = mapped_column(
        Enum(PhaseType),
        nullable=False,
        comment="Job phase",
    )

    label: Mapped[str] = mapped_column(
        String(job_resources["label"]["MAX_LENGTH"]),
        nullable=False,
        comment="Job label",
    )

    description: Mapped[str | None] = mapped_column(
        String(job_resources["description"]["MAX_LENGTH"]),
        nullable=True,
        comment="Job description",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Job creation datetime",
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Job execution start datetime",
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Job execution end datetime",
    )

    execution_duration: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Job execution duration",
    )
