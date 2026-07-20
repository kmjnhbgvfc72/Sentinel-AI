import json
from collections import Counter
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import Report, SecurityLog
from backend.models.user import utc_now


class ReportService:
    def __init__(self, db: Session): self.db = db

    def list(self) -> list[Report]:
        return list(self.db.scalars(select(Report).order_by(Report.created_at.desc())).all())

    def get(self, report_id: int) -> Report | None: return self.db.get(Report, report_id)

    def generate(self, report_type: str, generated_by: str) -> Report:
        logs = list(self.db.scalars(select(SecurityLog).where(SecurityLog.timestamp >= utc_now() - timedelta(days=1)).order_by(SecurityLog.timestamp.desc())).all())
        severity = Counter(log.severity for log in logs); types = Counter(log.event_type for log in logs)
        login_logs = [log for log in logs if "login" in log.event_type.lower()]
        summary = {
            "window": "last_24_hours", "total_security_events": len(logs), "total_logins": len(login_logs),
            "successful_logins": sum("success" in log.event_type.lower() for log in login_logs),
            "failed_logins": sum("fail" in log.event_type.lower() for log in login_logs),
            "detected_threats": sum(1 for log in logs if log.severity in {"high", "critical"}),
            "alerts": severity.get("critical", 0) + severity.get("high", 0), "incidents": severity.get("critical", 0),
            "severity": dict(severity), "threat_types": dict(types),
            "events": [{"type": log.event_type, "risk_level": log.severity, "source_ip": log.source_ip, "time": log.timestamp.isoformat()} for log in logs[:50]],
        }
        item = Report(report_type=report_type, generated_by=generated_by, summary=json.dumps(summary))
        self.db.add(item); self.db.commit(); self.db.refresh(item)
        return item
