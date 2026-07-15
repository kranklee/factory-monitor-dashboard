from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import AdminUser, CurrentUser, OperatorUser, SessionDep
from app.models.enums import MachineStatus
from app.schemas.common import Page
from app.schemas.machine import MachineCreate, MachineResponse, MachineUpdate
from app.services.machines import MachineService

router = APIRouter(prefix="/machines", tags=["Machines"])


@router.get("", response_model=Page[MachineResponse])
async def list_machines(
    session: SessionDep,
    _: CurrentUser,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(max_length=120)] = None,
    machine_status: Annotated[MachineStatus | None, Query(alias="status")] = None,
    location: Annotated[str | None, Query(max_length=120)] = None,
) -> Page[MachineResponse]:
    return await MachineService(session).list_machines(
        page, page_size, search, machine_status, location
    )


@router.get("/{machine_id}", response_model=MachineResponse)
async def get_machine(machine_id: int, session: SessionDep, _: CurrentUser) -> MachineResponse:
    return await MachineService(session).get_machine(machine_id)


@router.post("", response_model=MachineResponse, status_code=status.HTTP_201_CREATED)
async def create_machine(data: MachineCreate, session: SessionDep, _: AdminUser) -> MachineResponse:
    return await MachineService(session).create_machine(data)


@router.patch("/{machine_id}", response_model=MachineResponse)
async def update_machine(
    machine_id: int, data: MachineUpdate, session: SessionDep, _: OperatorUser
) -> MachineResponse:
    return await MachineService(session).update_machine(machine_id, data)
