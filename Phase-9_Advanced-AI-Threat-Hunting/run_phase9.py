"""Phase 9 FastAPI composition root and executable entry point."""
from dataclasses import dataclass, field
from hmac import compare_digest
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

from ai_learning.anomaly_learning import AnomalyLearner
from ai_learning.feedback_engine import FeedbackEngine
from ai_learning.model_retraining import ModelRetrainer
from ai_learning.model_versioning import ModelRegistry
from ai_learning.self_learning import SelfLearningEngine
from analytics.executive_dashboard import ExecutiveDashboard
from api import analytics_api, hunting_api, intelligence_api, learning_api, prediction_api
from automation.incident_manager import IncidentManager
from config.environment import validate_environment
from config.settings import Settings, get_settings
from prediction.attack_forecast import AttackForecaster
from prediction.attack_path_predictor import AttackPathPredictor
from prediction.risk_forecast import RiskForecaster
from threat_hunting.hunter import ThreatHunter
from threat_hunting.ioc_engine import IOCEngine
from threat_intelligence.intelligence_processor import IntelligenceProcessor
from threat_intelligence.ioc_database import IOCDatabase

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@dataclass
class Services:
    """Application-scoped dependency container."""
    iocs: IOCDatabase
    intelligence: IntelligenceProcessor
    hunter: ThreatHunter
    feedback: FeedbackEngine
    registry: ModelRegistry
    learning: SelfLearningEngine
    retrainer: ModelRetrainer
    attack_forecaster: AttackForecaster = field(default_factory=AttackForecaster)
    path_predictor: AttackPathPredictor = field(default_factory=AttackPathPredictor)
    risk_forecaster: RiskForecaster = field(default_factory=RiskForecaster)
    incidents: IncidentManager = field(default_factory=IncidentManager)
    dashboard: ExecutiveDashboard = field(default_factory=ExecutiveDashboard)
    events: list[dict[str, object]] = field(default_factory=list)
    current_risk: float = 0.0


def build_services(settings: Settings) -> Services:
    iocs, feedback, registry = IOCDatabase(), FeedbackEngine(), ModelRegistry()
    learning = SelfLearningEngine(AnomalyLearner(settings.anomaly_contamination), feedback, registry)
    return Services(iocs, IntelligenceProcessor(), ThreatHunter(IOCEngine(iocs)), feedback, registry, learning, ModelRetrainer(learning))


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    environment = validate_environment(settings)
    app = FastAPI(title=settings.app_name, version="9.0.0", description="Enterprise defensive threat hunting, intelligence, prediction, automation, analytics, and continuous learning API.")
    app.state.services = build_services(settings)
    app.state.environment_status = environment
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-API-Key"])

    async def authorize(request: Request, supplied: str | None = Depends(api_key_header)) -> None:
        if settings.api_key and (not supplied or not compare_digest(supplied, settings.api_key)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid API key")

    protected = [Depends(authorize)]
    for router in (hunting_api.router, intelligence_api.router, prediction_api.router, analytics_api.router, learning_api.router):
        app.include_router(router, prefix="/api/v1", dependencies=protected)

    @app.get("/health", tags=["Operations"])
    async def health() -> dict[str, object]:
        return {"status": "healthy", "version": "9.0.0", "environment_valid": environment.valid, "warnings": environment.warnings}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    active = get_settings()
    uvicorn.run("run_phase9:app", host=active.host, port=active.port, reload=active.debug)
