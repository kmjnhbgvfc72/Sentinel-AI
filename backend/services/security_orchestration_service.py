from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import AIDetection, AttackPath, Incident, SecurityLog, ThreatEvent
from backend.services.risk_service import RiskAssessment


class SecurityOrchestrationService:
    """Durable central fallback for Phase-4 detection, Phase-5 prediction, and Phase-6 response."""

    def __init__(self, db: Session):
        self.db = db

    def record_ai_detection(self, log: SecurityLog, assessment: RiskAssessment) -> AIDetection:
        existing = self.db.scalar(select(AIDetection).where(AIDetection.security_log_id == log.id))
        if existing:
            return existing
        summary = (
            f"Authentication behavior: {assessment.failed_attempts} failed attempts, "
            f"{assessment.login_frequency} logins, {assessment.distinct_usernames} usernames from source IP."
        )
        detection = AIDetection(
            security_log_id=log.id,
            risk_score=assessment.score,
            threat_level=assessment.level,
            behavior_summary=summary,
        )
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(detection)
        return detection

    def process_threat(self, threat: ThreatEvent) -> tuple[AttackPath, Incident | None]:
        attack_path = self.db.scalar(select(AttackPath).where(AttackPath.threat_event_id == threat.id))
        if not attack_path:
            path = "Failed Login Attempts → Account Compromise Risk → Privilege Escalation Risk → Sensitive Asset Exposure"
            attack_path = AttackPath(
                threat_event_id=threat.id,
                source_ip=threat.source_ip,
                path=path,
                risk_score=threat.risk_score,
                risk_level=threat.risk_level,
                status="PREDICTED",
            )
            self.db.add(attack_path)

        incident = None
        if threat.risk_level == "HIGH":
            cutoff = datetime.now(timezone.utc) - timedelta(minutes=5)
            incident = self.db.scalar(select(Incident).where(
                Incident.incident_type == threat.threat_type,
                Incident.status.in_(("OPEN", "IN_PROGRESS")),
                Incident.created_at >= cutoff,
            ))
            if not incident:
                incident = Incident(
                    incident_type=threat.threat_type,
                    severity="HIGH",
                    status="OPEN",
                    response_action="Incident recorded; response workflow started; administrator notification queued; defensive containment prepared.",
                )
                self.db.add(incident)
        self.db.commit()
        self.db.refresh(attack_path)
        if incident:
            self.db.refresh(incident)
        return attack_path, incident
