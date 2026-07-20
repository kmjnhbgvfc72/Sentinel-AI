from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Cyber Threat Detection Engine"
    app_version: str = "4.0.0"
    environment: str = "development"
    database_url: str = "sqlite:///./ai_detection.db"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://localhost:5175"])
    phase3_api_url: str = "http://127.0.0.1:8001/api"
    request_timeout_seconds: float = Field(default=8, ge=1, le=30)
    model_directory: Path = Path("../ai_models/trained_models")
    model_metadata_path: Path = Path("../ai_models/model_metadata.json")
    auto_analyze_phase3: bool = False
    demo_data_enabled: bool = True
    alert_risk_threshold: float = Field(default=70, ge=0, le=100)

    model_config = SettingsConfigDict(env_file="../.env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
