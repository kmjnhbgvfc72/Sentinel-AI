from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.database import get_db
from backend.models import Alert, User

router = APIRouter(prefix="/alerts", tags=["Security alerts"])


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    alert_type: str
    severity: str
    username: str
    ip_address: str
    description: str
    status: str
    attempt_count: int | None
    created_at: datetime


class AlertListResponse(BaseModel):
    data: list[AlertResponse]
    total: int
    limit: int
    offset: int


@router.get("", response_model=AlertListResponse)
def list_alerts(
    alert_status: str = Query(default="ACTIVE", alias="status", max_length=20),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    _: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> AlertListResponse:
    filters = [Alert.status == alert_status.upper()] if alert_status else []
    total = db.scalar(select(func.count(Alert.id)).where(*filters)) or 0
    rows = list(db.scalars(select(Alert).where(*filters).order_by(Alert.created_at.desc()).offset(offset).limit(limit)).all())
    return AlertListResponse(data=rows, total=total, limit=limit, offset=offset)
