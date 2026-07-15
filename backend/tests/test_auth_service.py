import pytest

from app.core.config import Settings
from app.core.exceptions import AuthenticationError
from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.services.auth import AuthService


async def test_login_returns_token_and_user_for_valid_credentials(session) -> None:
    session.add(
        User(
            email="operator@example.com",
            full_name="Test Operator",
            role=UserRole.OPERATOR,
            hashed_password=hash_password("ValidPass123!"),
        )
    )
    await session.commit()

    result = await AuthService(session, Settings()).login(
        LoginRequest(email="operator@example.com", password="ValidPass123!")
    )

    assert result.access_token
    assert result.user.role == UserRole.OPERATOR


async def test_login_rejects_invalid_password(session) -> None:
    session.add(
        User(
            email="viewer@example.com",
            full_name="Test Viewer",
            role=UserRole.VIEWER,
            hashed_password=hash_password("ValidPass123!"),
        )
    )
    await session.commit()

    with pytest.raises(AuthenticationError):
        await AuthService(session, Settings()).login(
            LoginRequest(email="viewer@example.com", password="WrongPass123!")
        )
