import json
from pathlib import Path

import httpx
from sqlalchemy.orm import Session

from app.ai_engine.prediction import ThreatPredictionEngine
from app.schemas import AnalysisResponse, SecurityEvent
from config.ai_settings import Settings
from database.ai_repository import AIRepository


class AIService:
    def __init__(self, session: Session, settings: Settings):
        self.settings = settings
        version = self._model_version(settings.model_metadata_path)
        self.engine = ThreatPredictionEngine(settings.model_directory, version)
        self.repository = AIRepository(session)

    @staticmethod
    def _model_version(path: Path) -> str:
        try:
            return str(json.loads(path.read_text(encoding="utf-8")).get("model_version", "4.0.0-fallback"))
        except (OSError, ValueError, TypeError):
            return "4.0.0-fallback"

    def analyze(self, event: SecurityEvent) -> AnalysisResponse:
        result, features = self.engine.analyze(event, self.settings.alert_risk_threshold)
        alert = None
        if result.alert_generated:
            alert = {"alert_type": result.threat_type, "description": f"AI analysis classified event {event.event_id} as {result.threat_type} with risk {result.risk_score}.", "priority": result.severity, "status": "new"}
        self.repository.save_analysis(event_id=event.event_id, prediction=result.threat_type, confidence=result.confidence, anomaly=result.anomaly, features=features, risk_score=result.risk_score, severity=result.severity, alert=alert)
        return result

    async def fetch_phase3_events(self, limit: int = 20) -> list[SecurityEvent]:
        async with httpx.AsyncClient(base_url=self.settings.phase3_api_url, timeout=self.settings.request_timeout_seconds) as client:
            logs_response, threats_response = await client.get("/logs", params={"page_size": limit}), await client.get("/threats", params={"page_size": limit})
            logs_response.raise_for_status()
            threats_response.raise_for_status()
        events = []
        for log in logs_response.json().get("data", []):
            details = log.get("details") or {}
            events.append(SecurityEvent(event_id=f"phase3-log-{log['id']}", event_type=log.get("event_type", "unknown"), severity=log.get("risk_level", "low"), failed_login_count=int(details.get("failed_login_count", 0)), unknown_ip=bool(details.get("unknown_ip", False)), abnormal_time=bool(details.get("abnormal_time", False)), activity_frequency=float(details.get("activity_frequency", 0)), historical_average=float(details.get("historical_average", 0))))
        for threat in threats_response.json().get("data", []):
            events.append(SecurityEvent(event_id=f"phase3-threat-{threat['id']}", event_type=threat.get("type", "unknown"), severity=threat.get("severity", "low"), ioc_reputation=float(threat.get("risk_score", 0)), historical_average=1, activity_frequency=1, malware_indicator="malware" in str(threat.get("type", "")).lower()))
        return events
