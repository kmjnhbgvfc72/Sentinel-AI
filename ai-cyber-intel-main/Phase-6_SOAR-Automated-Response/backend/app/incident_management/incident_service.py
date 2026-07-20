from models import AuditLog, Incident
from sqlalchemy import select


class IncidentService:
    def __init__(self, session):
        self.session = session

    def create(self, data, actor="system"):
        incident = Incident(**data)
        self.session.add(incident)
        self.session.flush()
        self.session.add(
            AuditLog(
                actor=actor,
                action="incident.created",
                resource=str(incident.id),
                details=incident.title,
            )
        )
        self.session.commit()
        self.session.refresh(incident)
        return incident

    def update(self, incident_id, changes, actor="system"):
        incident = self.session.get(Incident, incident_id)
        if not incident:
            return None
        for key, value in changes.items():
            setattr(incident, key, value)
        self.session.add(
            AuditLog(
                actor=actor,
                action="incident.updated",
                resource=str(incident_id),
                details=str(changes),
            )
        )
        self.session.commit()
        self.session.refresh(incident)
        return incident

    def list(self, limit=100):
        return list(
            self.session.scalars(
                select(Incident).order_by(Incident.created_at.desc()).limit(limit)
            )
        )
