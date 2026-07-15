from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import UserRole

if TYPE_CHECKING:
    from app.models.alert import Alert


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False, length=20), default=UserRole.VIEWER, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    acknowledged_alerts: Mapped[list["Alert"]] = relationship(back_populates="acknowledged_by")
