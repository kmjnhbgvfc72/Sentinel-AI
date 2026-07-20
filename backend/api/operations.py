from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.database import get_db
from backend.models import AIDetection, AttackPath, Incident, User

router = APIRouter(tags=["Central security operations"])


class DetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    security_log_id: int
    risk_score: int
    threat_level: Literal["LOW", "MEDIUM", "HIGH"]
    behavior_summary: str
    created_at: datetime


class AttackPathResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    threat_event_id: int
    source_ip: str
    path: str
    risk_score: int
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    status: str
    created_at: datetime


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    incident_type: str
    severity: str
    status: str
    response_action: str
    created_at: datetime


@router.get("/detections", response_model=list[DetectionResponse])
def detections(limit: int = Query(default=20, ge=1, le=200), _: User = Depends(current_user), db: Session = Depends(get_db)) -> list[AIDetection]:
    return list(db.scalars(select(AIDetection).order_by(AIDetection.created_at.desc()).limit(limit)).all())


@router.get("/attack-paths", response_model=list[AttackPathResponse])
def attack_paths(limit: int = Query(default=20, ge=1, le=200), _: User = Depends(current_user), db: Session = Depends(get_db)) -> list[AttackPath]:
    return list(db.scalars(select(AttackPath).order_by(AttackPath.created_at.desc()).limit(limit)).all())


@router.get("/incidents", response_model=list[IncidentResponse])
def incidents(
    incident_status: str | None = Query(default=None, alias="status", max_length=30),
    limit: int = Query(default=20, ge=1, le=200),
    _: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> list[Incident]:
    filters = [Incident.status == incident_status.upper()] if incident_status else []
    return list(db.scalars(select(Incident).where(*filters).order_by(Incident.created_at.desc()).limit(limit)).all())
