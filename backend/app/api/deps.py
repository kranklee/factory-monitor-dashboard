from collections.abc import Callable
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.users import UserRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    session: SessionDep,
    settings: SettingsDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if not credentials:
        raise AuthenticationError("Authentication required")
    try:
        payload = decode_access_token(credentials.credentials, settings)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError) as exc:
        raise AuthenticationError("Invalid or expired token") from exc

    user = await UserRepository(session).get_by_id(user_id)
    if not user or not user.is_active:
        raise AuthenticationError("User account is unavailable")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: UserRole) -> Callable[..., User]:
    async def role_dependency(user: CurrentUser) -> User:
        if user.role not in roles:
            raise AuthorizationError()
        return user

    return role_dependency


OperatorUser = Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))]
AdminUser = Annotated[User, Depends(require_roles(UserRole.ADMIN))]
