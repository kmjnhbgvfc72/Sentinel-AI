from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas import IncidentIn, ResponseIn
from database.connection import get_db
from security.access_control import require_permission
from security.authentication import Principal
from threat_response.executor import ResponseExecutor
from threat_response.incident_response import create_incident

router = APIRouter(prefix="/responses", tags=["Response"])


@router.post("/execute")
def execute(payload: ResponseIn, db: Session = Depends(get_db), principal: Principal = Depends(require_permission("response:execute"))):
    try:
        result = ResponseExecutor().execute(db, payload.action, payload.target, principal.username, payload.approved)
        return result.__dict__
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/incidents", status_code=201)
def incident(payload: IncidentIn, db: Session = Depends(get_db), _=Depends(require_permission("incident:write"))):
    row = create_incident(db, **payload.model_dump())
    return {"id": row.id, "status": row.status}

