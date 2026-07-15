from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.exceptions import AuthenticationError
from app.core.security import create_access_token, verify_password
from app.repositories.users import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse


class AuthService:
    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.users = UserRepository(session)
        self.settings = settings

    async def login(self, credentials: LoginRequest) -> TokenResponse:
        user = await self.users.get_by_email(credentials.email)
        if not user or not user.is_active:
            raise AuthenticationError()
        if not verify_password(credentials.password, user.hashed_password):
            raise AuthenticationError()

        token = create_access_token(str(user.id), user.role.value, self.settings)
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )
