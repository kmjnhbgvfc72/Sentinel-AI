from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Cyber Attack Path Prediction Engine"
    app_version: str = "5.0.0"
    environment: str = "development"
    database_url: str = "sqlite:///./attack_prediction.db"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://localhost:5176"])
    phase4_api_url: str = "http://127.0.0.1:8002/api"
    request_timeout_seconds: float = Field(default=8, ge=1, le=30)
    model_directory: Path = Path("../ai_models/trained_models")
    model_metadata_path: Path = Path("../ai_models/model_metadata.json")
    auto_analyze_phase4: bool = False
    demo_data_enabled: bool = True

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
