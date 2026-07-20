from sqlalchemy.orm import Session
from database.models import Incident


def create_incident(db: Session, title: str, severity: str, evidence: dict, actions: list | None = None) -> Incident:
    incident = Incident(title=title, severity=severity, evidence=evidence, actions=actions or [])
    db.add(incident); db.commit(); db.refresh(incident)
    return incident

