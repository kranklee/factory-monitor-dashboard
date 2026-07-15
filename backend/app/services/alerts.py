from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidStateError, NotFoundError
from app.models.alert import Alert
from app.models.enums import AlertSeverity, AlertStatus
from app.models.user import User
from app.repositories.alerts import AlertRepository
from app.schemas.alert import AlertResponse
from app.schemas.common import Page


def to_alert_response(alert: Alert) -> AlertResponse:
    return AlertResponse(
        id=alert.id,
        machine_id=alert.machine_id,
        machine_code=alert.machine.code,
        machine_name=alert.machine.name,
        severity=alert.severity,
        status=alert.status,
        title=alert.title,
        message=alert.message,
        detected_at=alert.detected_at,
        acknowledged_at=alert.acknowledged_at,
        acknowledged_by_id=alert.acknowledged_by_id,
        resolved_at=alert.resolved_at,
    )


class AlertService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.alerts = AlertRepository(session)

    async def list_alerts(
        self,
        page: int,
        page_size: int,
        search: str | None,
        status: AlertStatus | None,
        severity: AlertSeverity | None,
        machine_id: int | None,
    ) -> Page[AlertResponse]:
        alerts, total = await self.alerts.list(
            page, page_size, search, status, severity, machine_id
        )
        return Page(
            items=[to_alert_response(alert) for alert in alerts],
            page=page,
            page_size=page_size,
            total=total,
        )

    async def update_status(
        self, alert_id: int, target_status: AlertStatus, user: User
    ) -> AlertResponse:
        alert = await self.alerts.get_by_id(alert_id)
        if not alert:
            raise NotFoundError("Alert not found")
        if target_status == alert.status:
            return to_alert_response(alert)
        if alert.status == AlertStatus.RESOLVED:
            raise InvalidStateError("Resolved alerts cannot be reopened")
        if target_status == AlertStatus.ACTIVE:
            raise InvalidStateError("Alerts cannot be returned to active status")

        now = datetime.now(UTC)
        if target_status == AlertStatus.ACKNOWLEDGED:
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_at = now
            alert.acknowledged_by_id = user.id
        elif target_status == AlertStatus.RESOLVED:
            if not alert.acknowledged_at:
                alert.acknowledged_at = now
                alert.acknowledged_by_id = user.id
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = now

        await self.session.commit()
        return to_alert_response(alert)
