from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI CTI Threat Intelligence"
    app_version: str = "7.0.0"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./threat_intelligence.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5177"]
    demo_data_enabled: bool = True
    feed_scheduler_enabled: bool = False
    feed_sync_interval_minutes: int = Field(default=60, ge=5, le=1440)
    feed_request_timeout_seconds: float = Field(default=10, ge=1, le=30)
    feed_max_bytes: int = Field(default=5_000_000, ge=1024, le=20_000_000)
    allow_private_feed_hosts: bool = False
    reputation_cache_ttl_seconds: int = Field(default=3600, ge=60)
    phase3_api_url: str = "http://127.0.0.1:8001/api"
    phase4_api_url: str = "http://127.0.0.1:8002/api"
    phase5_api_url: str = "http://127.0.0.1:8003/api"
    phase6_api_url: str = "http://127.0.0.1:8004/api"
    integration_timeout_seconds: float = Field(default=3, ge=1, le=15)
    abuseipdb_api_key: str | None = None
    virustotal_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
