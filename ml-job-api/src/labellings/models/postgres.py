from sqlalchemy import (
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.common.models import BasePostgresModel
from src.labellings.resources import labelling_resources
from src.labellings.types import SpectrumSetType


class LabellingPostgresModel(BasePostgresModel):
    """
    SQLAlchemy ORM model for the `labellings` table.
    """

    __tablename__ = "labellings"

    repr_columns = (
        "labelling_id",
        "job_id",
        "spectrum_filename",
        "spectrum_set",
    )

    labelling_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        comment="Labelling ID",
    )

    job_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.job_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Job ID",
    )

    spectrum_filename: Mapped[str] = mapped_column(
        String(labelling_resources["spectrum_filename"]["MAX_LENGTH"]),
        nullable=False,
        comment="Spectrum filename",
    )

    spectrum_set: Mapped[SpectrumSetType] = mapped_column(
        Enum(SpectrumSetType),
        nullable=False,
        comment="Spectrum set",
    )

    sequence_iteration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Sequence iteration",
    )

    model_prediction: Mapped[str | None] = mapped_column(
        String(labelling_resources["model_prediction"]["MAX_LENGTH"]),
        nullable=True,
        comment="Model prediction",
    )

    user_label: Mapped[str | None] = mapped_column(
        String(labelling_resources["user_label"]["MAX_LENGTH"]),
        nullable=True,
        comment="User label",
    )

    user_comment: Mapped[str | None] = mapped_column(
        String(labelling_resources["user_comment"]["MAX_LENGTH"]),
        nullable=True,
        comment="User comment",
    )
