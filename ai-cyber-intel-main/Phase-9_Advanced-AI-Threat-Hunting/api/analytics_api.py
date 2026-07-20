"""Analytics REST routes."""
from typing import Any
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from analytics.statistics import detection_statistics
from analytics.trend_analysis import TrendAnalyzer

router = APIRouter(prefix="/analytics", tags=["Analytics"])


class AnalyticsRequest(BaseModel):
    events: list[dict[str, Any]] = Field(default_factory=list, max_length=10_000)


@router.post("/summary")
async def summary(payload: AnalyticsRequest) -> dict[str, object]:
    return {"statistics": detection_statistics(payload.events), "trends": TrendAnalyzer().analyze(payload.events)}


@router.get("/dashboard")
async def dashboard(request: Request) -> dict[str, object]:
    services = request.app.state.services
    statistics = detection_statistics(services.events)
    return services.dashboard.build(statistics, services.current_risk, services.incidents.list())
