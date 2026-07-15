from typing import Annotated

from fastapi import APIRouter, Query

from app.api.deps import CurrentUser, OperatorUser, SessionDep
from app.models.enums import AlertSeverity, AlertStatus
from app.schemas.alert import AlertResponse, AlertStatusUpdate
from app.schemas.common import Page
from app.services.alerts import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=Page[AlertResponse])
async def list_alerts(
    session: SessionDep,
    _: CurrentUser,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(max_length=120)] = None,
    alert_status: Annotated[AlertStatus | None, Query(alias="status")] = None,
    severity: AlertSeverity | None = None,
    machine_id: int | None = None,
) -> Page[AlertResponse]:
    return await AlertService(session).list_alerts(
        page, page_size, search, alert_status, severity, machine_id
    )


@router.patch("/{alert_id}/status", response_model=AlertResponse)
async def update_alert_status(
    alert_id: int,
    data: AlertStatusUpdate,
    session: SessionDep,
    user: OperatorUser,
) -> AlertResponse:
    return await AlertService(session).update_status(alert_id, data.status, user)
