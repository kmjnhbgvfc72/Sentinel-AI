from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    environment: str = "development"
    database_url: str = "sqlite:///./soc.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "development-only-change-this-secret"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    encryption_key: str | None = None
    model_path: str = "models/threat_model.joblib"
    auto_response_enabled: bool = False
    allowed_origins: list[str] = Field(default=["http://localhost:3000"])
    trusted_hosts: list[str] = Field(default=["localhost", "127.0.0.1", "testserver"])
    log_level: str = "INFO"
    admin_username: str = "admin"
    admin_password_hash: str = ""

    @field_validator("allowed_origins", "trusted_hosts", mode="before")
    @classmethod
    def split_csv(cls, value):
        return [part.strip() for part in value.split(",") if part.strip()] if isinstance(value, str) else value

    def validate_production(self) -> None:
        if self.environment == "production" and (len(self.jwt_secret) < 32 or "change" in self.jwt_secret.lower()):
            raise RuntimeError("JWT_SECRET must be a strong external secret in production")


@lru_cache
def get_settings() -> Settings:
    return Settings()

