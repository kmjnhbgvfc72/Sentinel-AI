from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.database import get_db
from backend.models import ThreatEvent, User

router = APIRouter(prefix="/threats", tags=["Authentication threat intelligence"])


class ThreatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    source_ip: str
    threat_type: str
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    risk_score: int
    description: str
    created_at: datetime


class ThreatListResponse(BaseModel):
    data: list[ThreatResponse]
    total: int
    limit: int
    offset: int


@router.get("", response_model=ThreatListResponse)
def list_threats(
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    _: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> ThreatListResponse:
    filters = [ThreatEvent.risk_level == risk_level] if risk_level else []
    total = db.scalar(select(func.count(ThreatEvent.id)).where(*filters)) or 0
    rows = list(db.scalars(
        select(ThreatEvent).where(*filters).order_by(ThreatEvent.created_at.desc()).offset(offset).limit(limit)
    ).all())
    return ThreatListResponse(data=rows, total=total, limit=limit, offset=offset)
