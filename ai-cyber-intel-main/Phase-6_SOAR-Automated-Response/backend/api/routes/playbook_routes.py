import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Playbook, Workflow
from app.playbooks.workflow_engine import ensure_playbooks, execute
from database.soar_repository import get_db

router = APIRouter(prefix="/playbooks", tags=["playbooks"])


@router.get("")
def playbooks(db: Session = Depends(get_db)):
    ensure_playbooks(db)
    return [
        {
            "id": p.id,
            "name": p.name,
            "trigger": p.trigger,
            "steps": json.loads(p.steps),
            "enabled": p.enabled,
        }
        for p in db.query(Playbook).all()
    ]


@router.post("/execute/{incident_id}")
def execute_playbook(
    incident_id: int, playbook_name: str | None = None, db: Session = Depends(get_db)
):
    ensure_playbooks(db)
    p = (
        db.query(Playbook).filter(Playbook.name == playbook_name).first()
        if playbook_name
        else db.query(Playbook).first()
    )
    return execute(db, incident_id, p)


@router.get("/workflows")
def workflows(db: Session = Depends(get_db)):
    return [
        {
            "id": w.id,
            "incident_id": w.incident_id,
            "playbook": w.playbook,
            "status": w.status,
            "steps_completed": w.steps_completed,
        }
        for w in db.query(Workflow).order_by(Workflow.id.desc()).all()
    ]
