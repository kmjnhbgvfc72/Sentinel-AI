from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SecurityEvent(BaseModel):
    event_id: str = Field(min_length=1, max_length=128)
    event_type: str = Field(default="unknown", max_length=100)
    severity: Literal["low", "medium", "high", "critical"] = "low"
    failed_login_count: int = Field(default=0, ge=0, le=10_000)
    ioc_reputation: float = Field(default=0, ge=0, le=100)
    vulnerability_score: float = Field(default=0, ge=0, le=10)
    activity_frequency: float = Field(default=0, ge=0, le=100_000)
    historical_average: float = Field(default=0, ge=0, le=100_000)
    unknown_ip: bool = False
    new_device: bool = False
    location_changed: bool = False
    abnormal_time: bool = False
    malware_indicator: bool = False
    data_access_volume: float = Field(default=0, ge=0, le=1_000_000_000)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def reject_sensitive_metadata(cls, value: dict[str, Any]) -> dict[str, Any]:
        forbidden = {"password", "token", "secret", "credential", "authorization", "cookie", "api_key"}
        if any(str(key).lower() in forbidden for key in value):
            raise ValueError("Sensitive credential fields are not accepted")
        return value


class AnalysisResponse(BaseModel):
    event_id: str
    anomaly: bool
    anomaly_score: float
    threat_type: str
    confidence: float
    risk_score: float
    severity: str
    behavior_flags: list[str]
    alert_generated: bool
    model_version: str


class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PredictionResponse(ORMResponse):
    id: int
    event_id: str
    prediction: str
    confidence_score: float
    anomaly: bool
    created_at: datetime


class RiskResponse(ORMResponse):
    id: int
    threat_id: str
    risk_score: float
    severity: str
    created_at: datetime


class AlertResponse(ORMResponse):
    id: int
    event_id: str
    alert_type: str
    description: str
    priority: str
    status: str
    created_at: datetime
