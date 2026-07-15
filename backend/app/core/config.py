from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Factory Monitor API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://factory:factory@localhost:5432/factory_monitor"
    jwt_secret_key: str = Field(
        default="development-only-change-me-use-a-secure-secret", min_length=32
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:4200"]
    log_level: str = "INFO"

    @field_validator("database_url", mode="before")
    @classmethod
    def use_async_postgresql_driver(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+asyncpg://", 1)
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
