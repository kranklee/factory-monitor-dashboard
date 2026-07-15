from fastapi import APIRouter

from app.api.deps import CurrentUser, SessionDep
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(session: SessionDep, _: CurrentUser) -> DashboardSummary:
    return await DashboardService(session).get_summary()
