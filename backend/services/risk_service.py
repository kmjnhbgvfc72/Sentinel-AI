from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import SecurityLog, ThreatEvent


@dataclass(frozen=True)
class RiskAssessment:
    level: str
    score: int
    failed_attempts: int
    login_frequency: int
    distinct_usernames: int


class RiskCalculationService:
    WINDOW_MINUTES = 5

    def __init__(self, db: Session):
        self.db = db

    def assess_identity(self, username: str, source_ip: str) -> RiskAssessment:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=self.WINDOW_MINUTES)
        base = (
            SecurityLog.event_type == "LOGIN",
            SecurityLog.ip_address == source_ip,
            SecurityLog.created_at >= cutoff,
        )
        login_frequency = self.db.scalar(select(func.count(SecurityLog.id)).where(*base)) or 0
        failed_attempts = self.db.scalar(select(func.count(SecurityLog.id)).where(
            *base, SecurityLog.username == username, SecurityLog.status == "FAILED",
        )) or 0
        distinct_usernames = self.db.scalar(select(func.count(func.distinct(SecurityLog.username))).where(*base)) or 0

        if failed_attempts > 5:
            level, score = "HIGH", 90
        elif failed_attempts >= 3 or login_frequency >= 10 or (distinct_usernames >= 3 and failed_attempts >= 1):
            level, score = "MEDIUM", 55
        elif failed_attempts:
            level, score = "MEDIUM", 35
        else:
            level, score = "LOW", 10
        return RiskAssessment(level, score, failed_attempts, login_frequency, distinct_usernames)

    def current_risk(self) -> dict:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=self.WINDOW_MINUTES)
        threats = list(self.db.scalars(
            select(ThreatEvent).where(ThreatEvent.created_at >= cutoff).order_by(ThreatEvent.created_at.desc())
        ).all())
        recent_failures = self.db.scalar(select(func.count(SecurityLog.id)).where(
            SecurityLog.event_type == "LOGIN",
            SecurityLog.status == "FAILED",
            SecurityLog.created_at >= cutoff,
        )) or 0
        baseline = 35 if recent_failures else 10
        score = max((threat.risk_score for threat in threats), default=baseline)
        level = "HIGH" if score >= 70 else "MEDIUM" if score >= 30 else "LOW"
        distribution = {name: sum(threat.risk_level == name for threat in threats) for name in ("LOW", "MEDIUM", "HIGH")}
        if not threats:
            distribution[level] = 1
        return {"risk_level": level, "risk_score": score, "events": threats, "distribution": distribution}
