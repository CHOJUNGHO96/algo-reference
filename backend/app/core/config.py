"""Application configuration using Pydantic BaseSettings"""

from typing import Optional
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Algorithm Reference Platform API"
    VERSION: str = "1.0.0"

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database Settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "algoref"
    POSTGRES_PORT: int = 5432
    POSTGRES_SCHEMA: str = "public"  # Default PostgreSQL schema
    DATABASE_URL: Optional[PostgresDsn] = None

    # Database Connection Settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    DB_CONNECT_TIMEOUT: int = 30
    DB_COMMAND_TIMEOUT: int = 60
    DB_SSL_MODE: bool = False

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> str:
        """Construct DATABASE_URL from components if not provided"""
        if isinstance(v, str):
            return v

        values = info.data
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=values.get("POSTGRES_DB", ""),
        ))

    # JWT Settings
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_f8d7e6c5b4a3928170"
    REFRESH_SECRET_KEY: str = "CHANGE_THIS_REFRESH_KEY_IN_PRODUCTION_a1b2c3d4e5f6"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days

    # Admin Settings
    FIRST_ADMIN_EMAIL: str = "admin@algoref.com"
    FIRST_ADMIN_PASSWORD: str = "admin123"  # Change in production

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )


settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance.

    This function is used for dependency injection in FastAPI
    and can be overridden in tests.
    """
    return settings
