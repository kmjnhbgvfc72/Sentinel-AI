from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

IOCType = Literal["ip", "domain", "url", "hash", "email"]
Severity = Literal["low", "medium", "high", "critical"]


class IOCInput(BaseModel):
    type: IOCType
    value: str = Field(min_length=1, max_length=2048)
    threat_type: str = Field(default="unknown", min_length=1, max_length=100)
    confidence: int = Field(default=50, ge=0, le=100)
    severity: Severity = "medium"
    source: str = Field(default="manual", min_length=1, max_length=120)
    tags: list[str] = Field(default_factory=list, max_length=20)
    expires_at: datetime | None = None


class IOCResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: str
    value: str
    threat_type: str
    confidence: int
    severity: str
    source: str
    tags: list
    active: bool
    first_seen: datetime
    last_seen: datetime
    expires_at: datetime | None


class FeedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    url: str
    format: str
    enabled: bool
    reliability: int
    created_at: datetime
    updated_at: datetime


class FeedSyncRequest(BaseModel):
    feed_ids: list[int] | None = None


class ReputationResponse(BaseModel):
    type: str
    value: str
    score: int
    verdict: str
    sources: list[str]
    details: dict
    cached: bool


class ErrorEnvelope(BaseModel):
    error: dict
