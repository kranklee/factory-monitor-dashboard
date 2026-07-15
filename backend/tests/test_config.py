from app.core.config import Settings


def test_render_postgresql_url_uses_asyncpg_driver() -> None:
    settings = Settings(database_url="postgresql://user:password@database.example.com/app")

    assert settings.database_url == "postgresql+asyncpg://user:password@database.example.com/app"


def test_async_database_url_is_not_modified() -> None:
    database_url = "postgresql+asyncpg://user:password@localhost/app"

    settings = Settings(database_url=database_url)

    assert settings.database_url == database_url
