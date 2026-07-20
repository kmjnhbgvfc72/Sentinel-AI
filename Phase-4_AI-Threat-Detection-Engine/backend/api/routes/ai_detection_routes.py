from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas import AlertResponse, AnalysisResponse, PredictionResponse, RiskResponse, SecurityEvent
from config.ai_settings import get_settings
from database.ai_repository import AIRepository, get_db
from services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI threat detection"])
settings = get_settings()


@router.post("/analyze", response_model=dict)
async def analyze_event(event: SecurityEvent, db: Session = Depends(get_db)) -> dict:
    result: AnalysisResponse = AIService(db, settings).analyze(event)
    return {"data": result.model_dump()}


@router.get("/predictions")
async def predictions(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)) -> dict:
    data = [PredictionResponse.model_validate(item).model_dump(mode="json") for item in AIRepository(db).predictions(limit)]
    return {"data": data, "meta": {"total": len(data), "limit": limit}}


@router.get("/risk-score")
async def risk_scores(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)) -> dict:
    data = [RiskResponse.model_validate(item).model_dump(mode="json") for item in AIRepository(db).risks(limit)]
    return {"data": data, "meta": {"total": len(data), "limit": limit}}


@router.get("/alerts")
async def alerts(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)) -> dict:
    data = [AlertResponse.model_validate(item).model_dump(mode="json") for item in AIRepository(db).alerts(limit)]
    return {"data": data, "meta": {"total": len(data), "limit": limit}}
