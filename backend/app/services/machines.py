from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.enums import MachineStatus
from app.repositories.machines import MachineRepository
from app.schemas.common import Page
from app.schemas.machine import MachineCreate, MachineResponse, MachineUpdate


class MachineService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.machines = MachineRepository(session)

    async def list_machines(
        self,
        page: int,
        page_size: int,
        search: str | None,
        status: MachineStatus | None,
        location: str | None,
    ) -> Page[MachineResponse]:
        machines, total = await self.machines.list(page, page_size, search, status, location)
        return Page(
            items=[MachineResponse.model_validate(machine) for machine in machines],
            page=page,
            page_size=page_size,
            total=total,
        )

    async def get_machine(self, machine_id: int) -> MachineResponse:
        machine = await self.machines.get_by_id(machine_id)
        if not machine:
            raise NotFoundError("Machine not found")
        return MachineResponse.model_validate(machine)

    async def create_machine(self, data: MachineCreate) -> MachineResponse:
        if await self.machines.get_by_code(data.code):
            raise ConflictError("A machine with this code already exists")
        machine = self.machines.add(data)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError("A machine with this code already exists") from exc
        await self.session.refresh(machine)
        return MachineResponse.model_validate(machine)

    async def update_machine(self, machine_id: int, data: MachineUpdate) -> MachineResponse:
        machine = await self.machines.get_by_id(machine_id)
        if not machine:
            raise NotFoundError("Machine not found")
        self.machines.update(machine, data)
        await self.session.commit()
        await self.session.refresh(machine)
        return MachineResponse.model_validate(machine)
