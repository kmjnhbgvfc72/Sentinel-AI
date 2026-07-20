from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.authentication.authentication import current_user
from app.schemas import IncidentCreate, IncidentOut, IncidentUpdate
from app.incident_management.incident_service import IncidentService
from database.soar_repository import get_db

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[IncidentOut])
def list_incidents(db: Session = Depends(get_db)):
    return IncidentService(db).list()


@router.post("", response_model=IncidentOut, status_code=201)
def create_incident(
    data: IncidentCreate,
    db: Session = Depends(get_db),
    actor: str = Depends(current_user),
):
    return IncidentService(db).create(data.model_dump(), actor)


@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident(
    incident_id: int,
    data: IncidentUpdate,
    db: Session = Depends(get_db),
    actor: str = Depends(current_user),
):
    result = IncidentService(db).update(
        incident_id, data.model_dump(exclude_none=True), actor
    )
    if not result:
        raise HTTPException(404, "Incident not found")
    return result
