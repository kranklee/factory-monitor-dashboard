from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import MachineStatus

if TYPE_CHECKING:
    from app.models.alert import Alert


class Machine(TimestampMixin, Base):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    location: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[MachineStatus] = mapped_column(
        Enum(MachineStatus, native_enum=False, length=20), index=True
    )
    temperature_celsius: Mapped[float] = mapped_column(Float)
    vibration_mm_s: Mapped[float] = mapped_column(Float)
    output_rate: Mapped[float] = mapped_column(Float)
    efficiency_percent: Mapped[float] = mapped_column(Float)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="machine", cascade="all, delete-orphan"
    )
