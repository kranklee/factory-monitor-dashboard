from pydantic import BaseModel

from app.models.enums import MachineStatus
from app.schemas.alert import AlertResponse


class StatusCount(BaseModel):
    status: MachineStatus
    count: int


class DashboardSummary(BaseModel):
    total_machines: int
    operational_machines: int
    active_alerts: int
    average_efficiency: float
    average_output_rate: float
    status_counts: list[StatusCount]
    recent_alerts: list[AlertResponse]
