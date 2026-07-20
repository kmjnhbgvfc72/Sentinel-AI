from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import Alert, SecurityLog, ThreatEvent
from backend.services.risk_service import RiskCalculationService
from backend.services.security_orchestration_service import SecurityOrchestrationService


class ThreatIntelligenceService:
    """Promotes suspicious central authentication patterns into durable SOC intelligence."""

    WINDOW_MINUTES = 5

    def __init__(self, db: Session):
        self.db = db
        self.risk = RiskCalculationService(db)

    def analyze_authentication(self, log: SecurityLog) -> ThreatEvent | None:
        source_ip = log.ip_address or log.source_ip
        assessment = self.risk.assess_identity(log.username, source_ip)
        orchestration = SecurityOrchestrationService(self.db)
        orchestration.record_ai_detection(log, assessment)
        if assessment.level == "LOW" or log.event_type != "LOGIN":
            return None

        brute_force = assessment.failed_attempts > 5
        suspicious_pattern = assessment.failed_attempts >= 3 or assessment.login_frequency >= 10 or assessment.distinct_usernames >= 3
        if not brute_force and not suspicious_pattern:
            return None

        threat_type = "BRUTE_FORCE_ATTACK" if brute_force else "SUSPICIOUS_LOGIN"
        description = "Brute force authentication pattern detected" if brute_force else "Suspicious IP and authentication behavior detected"
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=self.WINDOW_MINUTES)
        existing = self.db.scalar(select(ThreatEvent).where(
            ThreatEvent.source_ip == source_ip,
            ThreatEvent.threat_type == threat_type,
            ThreatEvent.created_at >= cutoff,
        ))
        if existing:
            orchestration.process_threat(existing)
            return existing

        threat = ThreatEvent(
            source_ip=source_ip,
            threat_type=threat_type,
            risk_level=assessment.level,
            risk_score=assessment.score,
            description=description,
        )
        self.db.add(threat)
        self._create_alert(log.username, source_ip, threat_type, assessment.failed_attempts, cutoff)
        self.db.commit()
        self.db.refresh(threat)
        orchestration.process_threat(threat)
        return threat

    def _create_alert(self, username: str, source_ip: str, threat_type: str, attempt_count: int, cutoff: datetime) -> None:
        existing = self.db.scalar(select(Alert.id).where(
            Alert.alert_type == threat_type,
            Alert.status == "ACTIVE",
            Alert.username == username,
            Alert.ip_address == source_ip,
            Alert.created_at >= cutoff,
        ))
        if existing:
            return
        description = (
            "Multiple failed authentication attempts detected"
            if threat_type == "BRUTE_FORCE_ATTACK"
            else "Suspicious authentication behavior detected"
        )
        self.db.add(Alert(
            alert_type=threat_type,
            severity="HIGH",
            username=username,
            ip_address=source_ip,
            description=description,
            status="ACTIVE",
            attempt_count=attempt_count,
        ))
