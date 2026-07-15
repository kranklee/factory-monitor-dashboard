from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import AlertSeverity, AlertStatus

if TYPE_CHECKING:
    from app.models.machine import Machine
    from app.models.user import User


class Alert(TimestampMixin, Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"), index=True)
    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity, native_enum=False, length=20), index=True
    )
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus, native_enum=False, length=20),
        default=AlertStatus.ACTIVE,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(160))
    message: Mapped[str] = mapped_column(Text)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    acknowledged_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    machine: Mapped["Machine"] = relationship(back_populates="alerts")
    acknowledged_by: Mapped["User | None"] = relationship(back_populates="acknowledged_alerts")
