import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select

from app.core.security import hash_password
from app.db.session import SessionFactory
from app.models.alert import Alert
from app.models.enums import AlertSeverity, AlertStatus, MachineStatus, UserRole
from app.models.machine import Machine
from app.models.user import User

USERS = [
    ("admin@factorymonitor.io", "Factory Administrator", UserRole.ADMIN, "Admin123!"),
    ("operator@factorymonitor.io", "Line Operator", UserRole.OPERATOR, "Operator123!"),
    ("viewer@factorymonitor.io", "Operations Viewer", UserRole.VIEWER, "Viewer123!"),
]

MACHINES = [
    (
        "CNC-101",
        "CNC Milling Center 1",
        "Machining Hall",
        MachineStatus.OPERATIONAL,
        61.4,
        2.1,
        46,
        94.2,
    ),
    (
        "CNC-102",
        "CNC Milling Center 2",
        "Machining Hall",
        MachineStatus.WARNING,
        78.8,
        4.9,
        39,
        81.5,
    ),
    ("PRS-201", "Hydraulic Press 1", "Press Shop", MachineStatus.OPERATIONAL, 52.1, 1.7, 31, 91.8),
    ("PRS-202", "Hydraulic Press 2", "Press Shop", MachineStatus.CRITICAL, 93.2, 8.4, 12, 42.6),
    (
        "ASM-301",
        "Assembly Robot 1",
        "Assembly Line A",
        MachineStatus.OPERATIONAL,
        44.9,
        1.2,
        68,
        96.1,
    ),
    ("ASM-302", "Assembly Robot 2", "Assembly Line A", MachineStatus.OFFLINE, 24.0, 0.0, 0, 0),
    ("PKG-401", "Packaging Cell 1", "Packaging", MachineStatus.OPERATIONAL, 38.6, 1.0, 112, 89.7),
    ("PKG-402", "Packaging Cell 2", "Packaging", MachineStatus.WARNING, 49.3, 3.8, 91, 76.9),
]


async def seed() -> None:
    now = datetime.now(UTC)
    async with SessionFactory() as session:
        for email, full_name, role, password in USERS:
            exists = await session.scalar(select(User.id).where(User.email == email))
            if not exists:
                session.add(
                    User(
                        email=email,
                        full_name=full_name,
                        role=role,
                        hashed_password=hash_password(password),
                    )
                )

        for index, machine_data in enumerate(MACHINES):
            code, name, location, status, temperature, vibration, output, efficiency = machine_data
            exists = await session.scalar(select(Machine.id).where(Machine.code == code))
            if not exists:
                session.add(
                    Machine(
                        code=code,
                        name=name,
                        location=location,
                        status=status,
                        temperature_celsius=temperature,
                        vibration_mm_s=vibration,
                        output_rate=output,
                        efficiency_percent=efficiency,
                        last_seen_at=now - timedelta(minutes=index * 3),
                    )
                )
        await session.commit()

        alert_count = await session.scalar(select(func.count(Alert.id)))
        if alert_count == 0:
            machine_rows = await session.execute(select(Machine))
            machines = {machine.code: machine for machine in machine_rows.scalars()}
            session.add_all(
                [
                    Alert(
                        machine_id=machines["PRS-202"].id,
                        severity=AlertSeverity.CRITICAL,
                        status=AlertStatus.ACTIVE,
                        title="Hydraulic pressure above limit",
                        message="Pressure has exceeded the safe operating threshold for 3 minutes.",
                        detected_at=now - timedelta(minutes=8),
                    ),
                    Alert(
                        machine_id=machines["CNC-102"].id,
                        severity=AlertSeverity.WARNING,
                        status=AlertStatus.ACTIVE,
                        title="Elevated spindle temperature",
                        message=(
                            "Spindle temperature is trending above the configured "
                            "warning threshold."
                        ),
                        detected_at=now - timedelta(minutes=24),
                    ),
                    Alert(
                        machine_id=machines["ASM-302"].id,
                        severity=AlertSeverity.WARNING,
                        status=AlertStatus.ACKNOWLEDGED,
                        title="Machine communication lost",
                        message="No telemetry has been received from the controller.",
                        detected_at=now - timedelta(hours=1, minutes=12),
                        acknowledged_at=now - timedelta(hours=1),
                    ),
                    Alert(
                        machine_id=machines["PKG-402"].id,
                        severity=AlertSeverity.INFO,
                        status=AlertStatus.RESOLVED,
                        title="Packaging material running low",
                        message="Material supply was replenished by the line operator.",
                        detected_at=now - timedelta(hours=3),
                        acknowledged_at=now - timedelta(hours=2, minutes=55),
                        resolved_at=now - timedelta(hours=2, minutes=40),
                    ),
                ]
            )
            await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
