from datetime import UTC, datetime

import pytest

from app.core.exceptions import InvalidStateError
from app.models.alert import Alert
from app.models.enums import AlertSeverity, AlertStatus, MachineStatus, UserRole
from app.models.machine import Machine
from app.models.user import User
from app.services.alerts import AlertService


async def test_operator_can_acknowledge_an_active_alert(session) -> None:
    user, alert = await create_alert_fixture(session, AlertStatus.ACTIVE)

    result = await AlertService(session).update_status(alert.id, AlertStatus.ACKNOWLEDGED, user)

    assert result.status == AlertStatus.ACKNOWLEDGED
    assert result.acknowledged_by_id == user.id
    assert result.acknowledged_at is not None


async def test_resolved_alert_cannot_be_reopened(session) -> None:
    user, alert = await create_alert_fixture(session, AlertStatus.RESOLVED)

    with pytest.raises(InvalidStateError, match="cannot be reopened"):
        await AlertService(session).update_status(alert.id, AlertStatus.ACKNOWLEDGED, user)


async def create_alert_fixture(session, status: AlertStatus) -> tuple[User, Alert]:
    now = datetime.now(UTC)
    user = User(
        email="operator@example.com",
        full_name="Operator",
        role=UserRole.OPERATOR,
        hashed_password="not-used",
    )
    machine = Machine(
        code="TEST-01",
        name="Test Machine",
        location="Test Bay",
        status=MachineStatus.WARNING,
        temperature_celsius=75,
        vibration_mm_s=4,
        output_rate=20,
        efficiency_percent=70,
        last_seen_at=now,
    )
    alert = Alert(
        machine=machine,
        severity=AlertSeverity.WARNING,
        status=status,
        title="Test alert",
        message="Test condition",
        detected_at=now,
        resolved_at=now if status == AlertStatus.RESOLVED else None,
    )
    session.add_all([user, machine, alert])
    await session.commit()
    return user, alert
