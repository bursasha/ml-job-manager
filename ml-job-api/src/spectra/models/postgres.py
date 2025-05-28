# from datetime import datetime
#
# from sqlalchemy import (
#     DateTime,
#     Enum,
#     Float,
#     String,
# )
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import (
#     Mapped,
#     mapped_column,
# )
#
# from src.infrastructure.models import BasePostgresModel
# from src.spectra.resources import spectrum_resources
# from src.spectra.types import SpectrumType
#
#
# class SpectrumPostgresModel(BasePostgresModel):
#     __tablename__ = "spectra"
#
#     updatable_columns = ()
#     repr_columns = (
#         "spectrum_id",
#         "filename",
#         "targetname",
#         "observed_at",
#     )
#
#     spectrum_id: Mapped[UUID] = mapped_column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         comment="Spectrum ID",
#     )
#
#     filename: Mapped[str] = mapped_column(
#         String(spectrum_resources["filename"]["MAX_LENGTH"]),
#         nullable=False,
#         unique=True,
#         comment="Spectrum filename",
#     )
#
#     dir_path: Mapped[str] = mapped_column(
#         String(spectrum_resources["dir_path"]["MAX_LENGTH"]),
#         nullable=False,
#         comment="Spectrum directory path",
#     )
#
#     targetname: Mapped[str] = mapped_column(
#         String(spectrum_resources["targetname"]["MAX_LENGTH"]),
#         nullable=False,
#         comment="Spectrum designation targetname",
#     )
#
#     observed_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         nullable=False,
#         comment="Spectrum observation datetime",
#     )
#
#     type: Mapped[SpectrumType] = mapped_column(
#         Enum(SpectrumType),
#         nullable=False,
#         comment="Spectrum class type",
#     )
#
#     subtype: Mapped[str] = mapped_column(
#         String(spectrum_resources["subtype"]["MAX_LENGTH"]),
#         nullable=False,
#         comment="Spectrum subclass type",
#     )
#
#     ra: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum right ascension",
#     )
#
#     dec: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum declination",
#     )
#
#     magtype: Mapped[str] = mapped_column(
#         String(spectrum_resources["magtype"]["MAX_LENGTH"]),
#         nullable=False,
#         comment="Spectrum magnitude type",
#     )
#
#     mag_1: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum magnitude 1 filter",
#     )
#
#     mag_2: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum magnitude 2 filter",
#     )
#
#     mag_3: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum magnitude 3 filter",
#     )
#
#     mag_4: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum magnitude 4 filter",
#     )
#
#     mag_5: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum magnitude 5 filter",
#     )
#
#     mag_6: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum magnitude 6 filter",
#     )
#
#     mag_7: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum magnitude 7 filter",
#     )
#
#     sn_u: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum signal and noise ratio (SNR) of u band",
#     )
#
#     sn_g: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum signal and noise ratio (SNR) of g band",
#     )
#
#     sn_r: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum signal and noise ratio (SNR) of r band",
#     )
#
#     sn_i: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum signal and noise ratio (SNR) of i band",
#     )
#
#     sn_z: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum signal and noise ratio (SNR) of z band",
#     )
#
#     z: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum redshift",
#     )
#
#     z_err: Mapped[float] = mapped_column(
#         Float,
#         nullable=False,
#         comment="Spectrum redshift error",
#     )
