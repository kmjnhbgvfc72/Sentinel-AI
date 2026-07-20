from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration; phase applications keep their own configuration."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CENTRAL_", extra="ignore")

    app_name: str = "AI Cyber Threat Intelligence - Central API"
    app_version: str = "1.0.0"
    environment: str = "development"
    database_url: str | None = None
    database_host: str = "localhost"
    database_port: int = Field(default=5432, ge=1, le=65_535)
    database_name: str = "cti_central"
    database_user: str = "cti"
    database_password: str = Field(default="cti", repr=False)
    request_timeout_seconds: float = Field(default=10, ge=1, le=60)
    cors_origins: str = "http://localhost:5173,http://localhost:8080"

    phase1_url: str = "http://127.0.0.1:8000"
    phase2_url: str = "http://127.0.0.1:8010"
    phase3_url: str = "http://127.0.0.1:8001"
    phase4_url: str = "http://127.0.0.1:8002"
    phase5_url: str = "http://127.0.0.1:8003"
    phase6_url: str = "http://127.0.0.1:8004"
    phase7_url: str = "http://127.0.0.1:8005"
    phase8_url: str = "http://127.0.0.1:8080"
    phase9_url: str = "http://127.0.0.1:8090"
    phase6_token: str | None = Field(default=None, repr=False)
    phase9_api_key: str | None = Field(default=None, repr=False)
    auth_token_ttl_minutes: int = Field(default=480, ge=15, le=10_080)
    trusted_location_header: str | None = None
    bootstrap_admin_username: str = "admin"
    bootstrap_admin_email: str = "admin@localhost"
    bootstrap_admin_password: str | None = Field(default=None, min_length=12, repr=False)

    @field_validator("bootstrap_admin_password", mode="before")
    @classmethod
    def empty_password_is_unset(cls, value: str | None) -> str | None:
        return value or None

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
