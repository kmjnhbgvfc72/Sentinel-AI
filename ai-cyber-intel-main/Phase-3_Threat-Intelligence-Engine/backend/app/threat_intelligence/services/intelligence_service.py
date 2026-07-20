from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.threat_intelligence.models import ActivityLog, Indicator, Vulnerability


class IntelligenceService:
    def __init__(self, session: Session):
        self.session = session

    def _list(self, model, *, page: int, page_size: int, filters: list, order_by):
        total = self.session.scalar(select(func.count()).select_from(model).where(*filters)) or 0
        records = self.session.scalars(select(model).where(*filters).order_by(order_by.desc()).offset((page - 1) * page_size).limit(page_size))
        return list(records), total

    def list_vulnerabilities(self, *, page: int, page_size: int, severity: str | None):
        return self._list(Vulnerability, page=page, page_size=page_size, filters=[Vulnerability.severity == severity] if severity else [], order_by=Vulnerability.published_at)

    def list_indicators(self, *, page: int, page_size: int, indicator_type: str | None):
        return self._list(Indicator, page=page, page_size=page_size, filters=[Indicator.indicator_type == indicator_type] if indicator_type else [], order_by=Indicator.last_seen_at)

    def list_logs(self, *, page: int, page_size: int, risk_level: str | None):
        return self._list(ActivityLog, page=page, page_size=page_size, filters=[ActivityLog.risk_level == risk_level] if risk_level else [], order_by=ActivityLog.created_at)
