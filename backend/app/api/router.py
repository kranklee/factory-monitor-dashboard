from fastapi import APIRouter

from app.api.routes import alerts, auth, dashboard, machines

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(machines.router)
api_router.include_router(alerts.router)
