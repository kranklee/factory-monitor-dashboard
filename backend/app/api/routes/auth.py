from fastapi import APIRouter

from app.api.deps import CurrentUser, SessionDep, SettingsDep
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest, session: SessionDep, settings: SettingsDep
) -> TokenResponse:
    return await AuthService(session, settings).login(credentials)


@router.get("/me", response_model=UserResponse)
async def get_profile(user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(user)
