import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(self, message: str, status_code: int, code: str) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND, "not_found")


class ConflictError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status.HTTP_409_CONFLICT, "conflict")


class AuthenticationError(AppError):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, "authentication_failed")


class AuthorizationError(AppError):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message, status.HTTP_403_FORBIDDEN, "forbidden")


class InvalidStateError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_CONTENT, "invalid_state")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
            headers=(
                {"WWW-Authenticate": "Bearer"} if isinstance(exc, AuthenticationError) else None
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        errors: list[dict[str, Any]] = []
        for error in exc.errors():
            errors.append(
                {
                    "field": ".".join(str(part) for part in error["loc"]),
                    "message": error["msg"],
                }
            )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Request validation failed",
                    "details": errors,
                }
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled application error", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "An unexpected error occurred",
                }
            },
        )
