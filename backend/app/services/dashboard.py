from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import MachineStatus
from app.repositories.alerts import AlertRepository
from app.repositories.machines import MachineRepository
from app.schemas.dashboard import DashboardSummary, StatusCount
from app.services.alerts import to_alert_response


class DashboardService:
    def __init__(self, session: AsyncSession) -> None:
        self.machines = MachineRepository(session)
        self.alerts = AlertRepository(session)

    async def get_summary(self) -> DashboardSummary:
        total, operational, average_efficiency, average_output, status_rows = (
            await self.machines.summary()
        )
        counts = dict(status_rows)
        recent_alerts = await self.alerts.recent()
        return DashboardSummary(
            total_machines=total,
            operational_machines=operational,
            active_alerts=await self.alerts.active_count(),
            average_efficiency=round(average_efficiency, 1),
            average_output_rate=round(average_output, 1),
            status_counts=[
                StatusCount(status=status, count=counts.get(status, 0)) for status in MachineStatus
            ],
            recent_alerts=[to_alert_response(alert) for alert in recent_alerts],
        )
