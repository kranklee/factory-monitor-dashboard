from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import AlertSeverity, AlertStatus


class AlertResponse(BaseModel):
    id: int
    machine_id: int
    machine_code: str
    machine_name: str
    severity: AlertSeverity
    status: AlertStatus
    title: str
    message: str
    detected_at: datetime
    acknowledged_at: datetime | None
    acknowledged_by_id: int | None
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class AlertStatusUpdate(BaseModel):
    status: AlertStatus
