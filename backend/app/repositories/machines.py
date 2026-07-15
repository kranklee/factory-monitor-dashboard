from __future__ import annotations

from sqlalchemy import Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import MachineStatus
from app.models.machine import Machine
from app.schemas.machine import MachineCreate, MachineUpdate


class MachineRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(
        self,
        page: int,
        page_size: int,
        search: str | None,
        status: MachineStatus | None,
        location: str | None,
    ) -> tuple[list[Machine], int]:
        query = self._filtered_query(search, status, location)
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.session.execute(count_query)).scalar_one()
        result = await self.session.execute(
            query.order_by(Machine.name).offset((page - 1) * page_size).limit(page_size)
        )
        return list(result.scalars()), total

    async def get_by_id(self, machine_id: int) -> Machine | None:
        return await self.session.get(Machine, machine_id)

    async def get_by_code(self, code: str) -> Machine | None:
        result = await self.session.execute(select(Machine).where(Machine.code == code))
        return result.scalar_one_or_none()

    def add(self, data: MachineCreate) -> Machine:
        machine = Machine(**data.model_dump())
        self.session.add(machine)
        return machine

    def update(self, machine: Machine, data: MachineUpdate) -> Machine:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(machine, field, value)
        return machine

    async def summary(self) -> tuple[int, int, float, float, list[tuple[MachineStatus, int]]]:
        totals = await self.session.execute(
            select(
                func.count(Machine.id),
                func.count(Machine.id).filter(Machine.status == MachineStatus.OPERATIONAL),
                func.coalesce(func.avg(Machine.efficiency_percent), 0),
                func.coalesce(func.avg(Machine.output_rate), 0),
            )
        )
        total, operational, average_efficiency, average_output = totals.one()
        status_result = await self.session.execute(
            select(Machine.status, func.count(Machine.id))
            .group_by(Machine.status)
            .order_by(Machine.status)
        )
        return (
            total,
            operational,
            float(average_efficiency),
            float(average_output),
            list(status_result.tuples()),
        )

    def _filtered_query(
        self,
        search: str | None,
        status: MachineStatus | None,
        location: str | None,
    ) -> Select[tuple[Machine]]:
        query = select(Machine)
        if search:
            term = f"%{search.strip()}%"
            query = query.where(or_(Machine.name.ilike(term), Machine.code.ilike(term)))
        if status:
            query = query.where(Machine.status == status)
        if location:
            query = query.where(Machine.location.ilike(f"%{location.strip()}%"))
        return query
