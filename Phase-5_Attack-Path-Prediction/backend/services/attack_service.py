import httpx
from sqlalchemy.orm import Session

from app.attack_engine.graph_analysis import GraphBuilder
from app.attack_engine.prediction import AttackPredictor
from app.attack_engine.response_engine import ResponsePlanner
from app.attack_engine.risk_engine import AssetRiskEngine
from app.schemas import AnalysisResponse, AttackEvent
from config.attack_settings import Settings
from database.attack_repository import AttackRepository


class AttackService:
    def __init__(self, session: Session, settings: Settings):
        self.settings = settings
        self.repository = AttackRepository(session)
        self.builder = GraphBuilder()
        self.predictor = AttackPredictor(settings.model_directory / "attack_prediction_model.pkl")
        self.risk_engine = AssetRiskEngine()
        self.planner = ResponsePlanner()

    def analyze(self, event: AttackEvent) -> AnalysisResponse:
        raw = event.model_dump()
        graph, edges = self.builder.build(raw)
        paths = self.predictor.predict(graph, raw)
        asset_names = list(dict.fromkeys([raw.get("target_asset") or "Database Server", raw.get("source_asset") or "Web Server"]))
        assets = self.risk_engine.calculate(raw, asset_names)
        recommendations = self.planner.plan(raw, assets)
        self.repository.save_analysis(paths, edges, assets, recommendations)
        return AnalysisResponse(event_id=event.event_id, paths=paths, affected_assets=assets, recommendations=recommendations)

    async def fetch_phase4_events(self, limit: int = 20) -> list[AttackEvent]:
        async with httpx.AsyncClient(base_url=self.settings.phase4_api_url, timeout=self.settings.request_timeout_seconds) as client:
            predictions = (await client.get("/ai/predictions", params={"limit": limit})).json().get("data", [])
            risks = (await client.get("/ai/risk-score", params={"limit": limit})).json().get("data", [])
        events = []
        for index, prediction in enumerate(predictions):
            risk = risks[index] if index < len(risks) else {}
            events.append(AttackEvent(event_id=f"phase4-{prediction['event_id']}", threat_type=prediction.get("prediction", "Unknown Threat"), severity=risk.get("severity", "medium"), confidence=prediction.get("confidence_score", 50), risk_score=risk.get("risk_score", 0), source_ip="AI-detected indicator", user="User Account", source_asset="Web Server", target_asset="Database Server", vulnerability="CVE-2026-41001" if risk.get("severity") in {"high", "critical"} else None, vulnerability_severity=risk.get("severity")))
        return events
