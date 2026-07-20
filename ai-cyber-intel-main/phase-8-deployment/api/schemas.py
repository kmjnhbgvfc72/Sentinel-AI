from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field, IPvAnyAddress


class ThreatIn(BaseModel):
    source: Literal["firewall", "server", "network", "edr", "threat-intel"]
    source_ip: IPvAnyAddress | None = None
    category: str = Field(min_length=2, max_length=64)
    severity: Literal["low", "medium", "high", "critical"]
    risk_score: float = Field(ge=0, le=100)
    details: dict[str, Any] = Field(default_factory=dict)


class PredictionIn(BaseModel):
    anomaly_score: float = Field(ge=0, le=1)
    asset_criticality: float = Field(ge=0, le=1)
    threat_confidence: float = Field(ge=0, le=1)
    exposure: float = Field(ge=0, le=1)
    asset: str | None = Field(default=None, max_length=128)


class AlertIn(BaseModel):
    threat_id: str | None = None
    title: str = Field(min_length=3, max_length=200)
    severity: Literal["low", "medium", "high", "critical"]
    description: str = Field(min_length=3, max_length=4000)


class ResponseIn(BaseModel):
    action: Literal["block_ip", "isolate_device", "disable_account"]
    target: str = Field(min_length=1, max_length=255)
    approved: bool = False
    reason: str = Field(min_length=5, max_length=1000)


class IncidentIn(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    severity: Literal["low", "medium", "high", "critical"]
    evidence: dict[str, Any] = Field(default_factory=dict)
    actions: list[str] = Field(default_factory=list, max_length=50)

