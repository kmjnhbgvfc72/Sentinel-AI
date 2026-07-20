"""Prediction REST routes."""
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/predictions", tags=["Predictions"])


class ForecastRequest(BaseModel):
    indicators: dict[str, float]
    horizon_hours: int = Field(default=24, ge=1, le=720)


class PathRequest(BaseModel):
    edges: list[dict[str, object]]
    start: str
    targets: list[str]


class RiskRequest(BaseModel):
    assets: list[dict[str, object]]


@router.post("/attacks")
async def attack_forecast(payload: ForecastRequest, request: Request) -> dict[str, object]:
    return request.app.state.services.attack_forecaster.forecast(payload.indicators, payload.horizon_hours)


@router.post("/paths")
async def attack_paths(payload: PathRequest, request: Request) -> list[dict[str, object]]:
    return request.app.state.services.path_predictor.predict(payload.edges, payload.start, payload.targets)


@router.post("/risk")
async def risk_forecast(payload: RiskRequest, request: Request) -> dict[str, object]:
    return request.app.state.services.risk_forecaster.forecast(payload.assets)
