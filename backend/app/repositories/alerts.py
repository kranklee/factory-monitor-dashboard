from __future__ import annotations

from sqlalchemy import Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.alert import Alert
from app.models.enums import AlertSeverity, AlertStatus
from app.models.machine import Machine


class AlertRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(
        self,
        page: int,
        page_size: int,
        search: str | None,
        status: AlertStatus | None,
        severity: AlertSeverity | None,
        machine_id: int | None,
    ) -> tuple[list[Alert], int]:
        query = self._filtered_query(search, status, severity, machine_id)
        total = (
            await self.session.execute(select(func.count()).select_from(query.subquery()))
        ).scalar_one()
        result = await self.session.execute(
            query.options(joinedload(Alert.machine))
            .order_by(Alert.detected_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars()), total

    async def get_by_id(self, alert_id: int) -> Alert | None:
        result = await self.session.execute(
            select(Alert).options(joinedload(Alert.machine)).where(Alert.id == alert_id)
        )
        return result.scalar_one_or_none()

    async def active_count(self) -> int:
        result = await self.session.execute(
            select(func.count(Alert.id)).where(Alert.status != AlertStatus.RESOLVED)
        )
        return result.scalar_one()

    async def recent(self, limit: int = 5) -> list[Alert]:
        result = await self.session.execute(
            select(Alert)
            .options(joinedload(Alert.machine))
            .order_by(Alert.detected_at.desc())
            .limit(limit)
        )
        return list(result.scalars())

    def _filtered_query(
        self,
        search: str | None,
        status: AlertStatus | None,
        severity: AlertSeverity | None,
        machine_id: int | None,
    ) -> Select[tuple[Alert]]:
        query = select(Alert).join(Machine)
        if search:
            term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Alert.title.ilike(term),
                    Alert.message.ilike(term),
                    Machine.name.ilike(term),
                    Machine.code.ilike(term),
                )
            )
        if status:
            query = query.where(Alert.status == status)
        if severity:
            query = query.where(Alert.severity == severity)
        if machine_id:
            query = query.where(Alert.machine_id == machine_id)
        return query
