import os

from pydantic_settings import BaseSettings, SettingsConfigDict


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and not url.startswith("postgresql+psycopg://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    is_postgres = url.startswith("postgresql")
    if is_postgres and "localhost" not in url and "sslmode=" not in url:
        joiner = "&" if "?" in url else "?"
        url = f"{url}{joiner}sslmode=require"
    return url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Shop API - FastAPI CRUD with PostgreSQL"
    database_url: str = "postgresql+psycopg://postgres:rwdy@localhost:5432/shop"

    def sqlalchemy_url(self) -> str:
        return _normalize_database_url(self.database_url)


settings = Settings(
    database_url=os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:rwdy@localhost:5432/shop")
)
