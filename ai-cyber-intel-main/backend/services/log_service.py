import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from backend.config import Settings
from backend.integrations.phase_client import PhaseClient
from backend.integrations.registry import build_registry
from backend.models import SecurityLog


class LogService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, values: dict[str, Any]) -> SecurityLog:
        log = SecurityLog(**values)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list(self, *, search: str | None, severity: str | None, event_type: str | None, limit: int, offset: int) -> tuple[list[SecurityLog], int]:
        filters = []
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(or_(SecurityLog.event_type.ilike(pattern), SecurityLog.username.ilike(pattern), SecurityLog.source_ip.ilike(pattern), SecurityLog.description.ilike(pattern)))
        if severity:
            filters.append(SecurityLog.severity == severity)
        if event_type:
            filters.append(SecurityLog.event_type == event_type)
        query = select(SecurityLog).where(*filters)
        total = self.db.scalar(select(func.count()).select_from(query.subquery())) or 0
        rows = self.db.scalars(query.order_by(SecurityLog.timestamp.desc()).offset(offset).limit(limit)).all()
        return list(rows), total


class SecurityPipeline:
    """Fault-tolerant bridge from a central security event to all phase capabilities."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.clients = {number: PhaseClient(phase, settings) for number, phase in build_registry(settings).items()}

    async def process(self, log: SecurityLog) -> dict[str, Any]:
        event_id = f"central-log-{log.id}"
        results: dict[str, Any] = {
            "phase_1": {"status": "stored", "capability": "foundation and PostgreSQL"},
            "phase_2": {"status": "available", "capability": "central SOC log display"},
        }
        ai_result = await self._request(4, "POST", "/api/ai/analyze", {
            "event_id": event_id,
            "event_type": log.event_type,
            "severity": log.severity,
            "unknown_ip": False,
            "abnormal_time": False,
            "metadata": {"username": log.username, "source_ip": log.source_ip, "description": log.description},
        })
        results["phase_3"] = await self._request(3, "GET", "/api/threat-statistics")
        results["phase_4"] = ai_result
        detection = ai_result.get("data", {}).get("data", {}) if ai_result.get("status") == "processed" else {}
        path_result = await self._request(5, "POST", "/api/attack/analyze", {
            "event_id": event_id,
            "threat_type": detection.get("threat_type", log.event_type),
            "severity": detection.get("severity", log.severity),
            "confidence": detection.get("confidence", 50),
            "risk_score": detection.get("risk_score", 0),
            "source_ip": log.source_ip,
            "user": log.username,
            "source_asset": log.source_ip,
            "target_asset": "SOC monitored environment",
        })
        results["phase_5"] = path_result
        if log.severity in {"high", "critical"}:
            results["phase_6"] = await self._request(6, "POST", "/api/incidents", {"title": f"{log.event_type} from {log.source_ip}", "description": log.description, "severity": log.severity, "source": "central-security-log"})
        else:
            results["phase_6"] = {"status": "observed", "capability": "SOAR threshold not reached"}
        results["phase_7"] = await self._request(7, "GET", "/api/correlation?refresh=true")
        results["phase_8"] = await self._request(8, "GET", "/health/ready")
        results["phase_9"] = await self._request(9, "POST", "/api/v1/hunting/search", {"id": event_id, "text": log.description, "behaviors": [log.event_type], "fields": {"username": log.username, "source_ip": log.source_ip, "severity": log.severity}})
        return results

    async def _request(self, phase: int, method: str, path: str, payload: dict | None = None) -> dict[str, Any]:
        try:
            kwargs = {"content": json.dumps(payload).encode(), "content_type": "application/json"} if payload is not None else {}
            response = await self.clients[phase].request(method, path, **kwargs)
            data = response.json() if response.headers.get("content-type", "").startswith("application/json") else None
            return {"status": "processed" if response.is_success else "degraded", "status_code": response.status_code, "data": data}
        except Exception as exc:
            return {"status": "unavailable", "status_code": None, "detail": str(exc)}
