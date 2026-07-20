from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Severity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ThreatResponse(ORMModel):
    id: int
    name: str
    type: str
    description: str
    severity: Severity
    risk_score: float = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=100)
    source: str
    status: str
    created_at: datetime


class VulnerabilityResponse(ORMModel):
    id: int
    cve_id: str
    description: str
    severity: Severity
    cvss_score: float | None
    risk_level: str
    affected_products: list[str]
    published_at: datetime


class IndicatorResponse(ORMModel):
    id: int
    indicator_type: str
    value: str
    confidence_score: float
    reputation_score: float | None
    threat_category: str
    country: str | None
    status: str
    first_seen_at: datetime
    last_seen_at: datetime


class ActivityLogResponse(ORMModel):
    id: int
    user_id: str
    event_type: str
    ip_address: str | None
    device: str | None
    status: str
    risk_level: Severity
    risk_score: float = Field(ge=0, le=100)
    details: dict
    created_at: datetime
