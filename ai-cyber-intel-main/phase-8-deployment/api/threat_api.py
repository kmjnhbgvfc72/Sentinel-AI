from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from ai_production.prediction_engine import PredictionEngine
from ai_production.risk_scoring import RiskFactors
from api.schemas import PredictionIn, ThreatIn
from database.connection import get_db
from database.models import Threat
from security.access_control import require_permission

router = APIRouter(prefix="/threats", tags=["Threats"])


@router.get("")
def list_threats(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db), _=Depends(require_permission("threat:read"))):
    rows = db.scalars(select(Threat).order_by(desc(Threat.detected_at)).limit(limit)).all()
    return [{"id": row.id, "source": row.source, "source_ip": row.source_ip, "category": row.category, "severity": row.severity, "risk_score": row.risk_score, "details": row.details, "detected_at": row.detected_at} for row in rows]


@router.post("", status_code=201)
def ingest_threat(payload: ThreatIn, db: Session = Depends(get_db), _=Depends(require_permission("alert:write"))):
    row = Threat(**payload.model_dump(mode="json")); db.add(row); db.commit(); db.refresh(row)
    return {"id": row.id, "status": "accepted"}


def prediction_router(engine: PredictionEngine):
    routes = APIRouter(prefix="/predictions", tags=["AI Predictions"])
    @routes.post("")
    def predict(payload: PredictionIn, _=Depends(require_permission("prediction:run"))):
        factors = RiskFactors(payload.anomaly_score, payload.asset_criticality, payload.threat_confidence, payload.exposure)
        return engine.predict(factors, payload.model_dump())
    return routes

