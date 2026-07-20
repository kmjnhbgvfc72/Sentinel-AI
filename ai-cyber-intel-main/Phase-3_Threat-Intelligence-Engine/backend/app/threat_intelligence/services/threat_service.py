from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.threat_intelligence.models import ActivityLog, Threat, Vulnerability


class ThreatService:
    def __init__(self, session: Session):
        self.session = session

    def list_threats(self, *, page: int, page_size: int, severity: str | None, threat_type: str | None) -> tuple[list[Threat], int]:
        filters = []
        if severity:
            filters.append(Threat.severity == severity)
        if threat_type:
            filters.append(Threat.type == threat_type)
        total = self.session.scalar(select(func.count()).select_from(Threat).where(*filters)) or 0
        records = self.session.scalars(select(Threat).where(*filters).order_by(Threat.created_at.desc()).offset((page - 1) * page_size).limit(page_size))
        return list(records), total

    def statistics(self) -> dict:
        rows = self.session.execute(select(Threat.severity, func.count(Threat.id)).group_by(Threat.severity)).all()
        by_severity = {severity: count for severity, count in rows}
        average = float(self.session.scalar(select(func.avg(Threat.risk_score))) or 0)
        return {"total_threats": sum(by_severity.values()), "high_risk_threats": by_severity.get("critical", 0) + by_severity.get("high", 0), "critical_alerts": by_severity.get("critical", 0), "critical_vulnerabilities": self.session.scalar(select(func.count()).select_from(Vulnerability).where(Vulnerability.severity == "critical")) or 0, "suspicious_events": self.session.scalar(select(func.count()).select_from(ActivityLog).where(ActivityLog.risk_level.in_(["high", "critical"]))) or 0, "average_risk_score": round(average, 1), "overall_risk_score": round(average, 1), "by_severity": {key: by_severity.get(key, 0) for key in ("critical", "high", "medium", "low")}}
