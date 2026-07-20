from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Cyber Threat Intelligence Engine"
    app_version: str = "3.0.0"
    environment: str = "development"
    database_url: str = "sqlite:///./threat_intelligence.db"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://localhost:5174"])
    demo_data_enabled: bool = True
    external_feeds_enabled: bool = False
    request_timeout_seconds: float = Field(default=10, ge=1, le=60)
    nvd_api_url: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    nvd_api_key: str | None = None

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
