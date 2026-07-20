from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class Severity(StrEnum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class AlertStatus(StrEnum):
    new = "new"
    investigating = "investigating"
    acknowledged = "acknowledged"
    resolved = "resolved"


class ThreatStatus(StrEnum):
    active = "active"
    investigating = "investigating"
    contained = "contained"
    resolved = "resolved"


class AlertStatusUpdate(BaseModel):
    status: AlertStatus
    changed_by: str = Field(default="soc-analyst", min_length=2, max_length=100)

    @field_validator("changed_by")
    @classmethod
    def sanitize_actor(cls, value: str) -> str:
        value = value.strip()
        if not value.replace("-", "").replace("_", "").isalnum():
            raise ValueError("changed_by may contain letters, numbers, hyphens, and underscores")
        return value


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime
