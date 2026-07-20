"""Typed Phase 9 application configuration."""
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from environment variables prefixed with ``PHASE9_``."""

    model_config = SettingsConfigDict(env_prefix="PHASE9_", env_file=".env", extra="ignore")
    app_name: str = "AI Cyber Threat Intelligence - Phase 9"
    environment: str = "development"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8090
    api_key: str | None = Field(default=None, repr=False)
    database_url: str = "postgresql+psycopg://phase9@localhost:5432/threat_intelligence"
    model_directory: Path = Path(".phase9/models")
    retraining_interval_seconds: int = Field(default=86_400, ge=60)
    anomaly_contamination: float = Field(default=0.05, gt=0, le=0.5)
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide cached configuration."""
    return Settings()
