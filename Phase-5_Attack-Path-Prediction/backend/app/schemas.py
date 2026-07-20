from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class AttackEvent(BaseModel):
    event_id: str = Field(min_length=1, max_length=128)
    threat_type: str = Field(default="Unknown Threat", max_length=100)
    severity: Literal["low", "medium", "high", "critical"] = "medium"
    confidence: float = Field(default=50, ge=0, le=100)
    risk_score: float = Field(default=0, ge=0, le=100)
    source_ip: str | None = Field(default=None, max_length=45)
    user: str | None = Field(default=None, max_length=160)
    source_asset: str | None = Field(default=None, max_length=160)
    target_asset: str | None = Field(default=None, max_length=160)
    vulnerability: str | None = Field(default=None, max_length=64)
    vulnerability_severity: Literal["low", "medium", "high", "critical"] | None = None
    criticality: int = Field(default=50, ge=0, le=100)
    historical_incidents: int = Field(default=0, ge=0, le=1000)


class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PathResponse(ORMResponse):
    id: int
    source_node: str
    destination_node: str
    path: str
    risk_score: float
    risk_level: str
    created_at: datetime


class AssetResponse(ORMResponse):
    id: int
    asset_name: str
    asset_type: str
    criticality: int
    risk_score: float


class RecommendationResponse(ORMResponse):
    id: int
    threat_id: str
    recommendation: str
    priority: str
    status: str
    created_at: datetime


class AnalysisResponse(BaseModel):
    event_id: str
    paths: list[dict[str, Any]]
    affected_assets: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]
