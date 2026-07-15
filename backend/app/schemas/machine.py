from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import MachineStatus


class MachineBase(BaseModel):
    code: str = Field(min_length=2, max_length=40, pattern=r"^[A-Z0-9-]+$")
    name: str = Field(min_length=2, max_length=120)
    location: str = Field(min_length=2, max_length=120)
    status: MachineStatus
    temperature_celsius: float = Field(ge=-50, le=300)
    vibration_mm_s: float = Field(ge=0, le=100)
    output_rate: float = Field(ge=0)
    efficiency_percent: float = Field(ge=0, le=100)
    last_seen_at: datetime


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    location: str | None = Field(default=None, min_length=2, max_length=120)
    status: MachineStatus | None = None
    temperature_celsius: float | None = Field(default=None, ge=-50, le=300)
    vibration_mm_s: float | None = Field(default=None, ge=0, le=100)
    output_rate: float | None = Field(default=None, ge=0)
    efficiency_percent: float | None = Field(default=None, ge=0, le=100)
    last_seen_at: datetime | None = None


class MachineResponse(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
