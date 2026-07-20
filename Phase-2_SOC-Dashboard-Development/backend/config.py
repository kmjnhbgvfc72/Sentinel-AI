from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Cyber Threat Intelligence SOC API"
    app_version: str = "2.0.0"
    environment: str = "development"
    cors_origins: list[str] = Field(default_factory=list)
    database_url: str | None = None
    demo_data_enabled: bool = True

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
