from fastapi import APIRouter, Query

from services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
async def get_summary() -> dict:
    return {"data": dashboard_service.summary()}


@router.get("/threat-trends")
async def get_threat_trends(range_key: str = Query("24h", alias="range", pattern="^(24h|7d|30d)$")) -> dict:
    return {"data": dashboard_service.threat_trends(range_key)}


@router.get("/risk-distribution")
async def get_risk_distribution() -> dict:
    return {"data": dashboard_service.risk_distribution()}


@router.get("/recent-alerts")
async def get_recent_alerts(limit: int = Query(5, ge=1, le=25)) -> dict:
    return {"data": dashboard_service.recent_alerts(limit)}


@router.get("/top-assets")
async def get_top_assets(limit: int = Query(5, ge=1, le=25)) -> dict:
    return {"data": dashboard_service.top_assets(limit)}
