from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from api.schemas import AlertIn
from database.connection import get_db
from database.models import Alert
from security.access_control import require_permission

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("")
def list_alerts(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db), _=Depends(require_permission("alert:read"))):
    rows = db.scalars(select(Alert).order_by(desc(Alert.created_at)).limit(limit)).all()
    return [{"id": r.id, "threat_id": r.threat_id, "title": r.title, "severity": r.severity, "status": r.status, "description": r.description, "created_at": r.created_at} for r in rows]


@router.post("", status_code=201)
def create_alert(payload: AlertIn, db: Session = Depends(get_db), _=Depends(require_permission("alert:write"))):
    row = Alert(**payload.model_dump()); db.add(row); db.commit(); db.refresh(row)
    return {"id": row.id, "status": row.status}

