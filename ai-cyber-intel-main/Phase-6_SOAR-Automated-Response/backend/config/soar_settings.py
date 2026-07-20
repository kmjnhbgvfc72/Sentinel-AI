from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "AI CTI SOAR"
    app_version: str = "6.0.0"
    database_url: str = "sqlite:///./soar.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5177"]
    admin_token: str = "change-me-in-env"
    phase4_api_url: str = "http://127.0.0.1:8002/api"
    phase5_api_url: str = "http://127.0.0.1:8003/api"
    demo_data_enabled: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
