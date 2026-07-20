"""AI learning REST routes."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/learning", tags=["AI Learning"])


class TrainingRequest(BaseModel):
    samples: list[list[float]] = Field(min_length=2, max_length=100_000)


class AssessmentRequest(BaseModel):
    features: list[float] = Field(min_length=1, max_length=1_000)


class FeedbackRequest(BaseModel):
    detection_id: str
    verdict: str
    rule_id: str = "unknown"


@router.post("/retrain")
async def retrain(payload: TrainingRequest, request: Request) -> dict[str, object]:
    try:
        return request.app.state.services.retrainer.retrain(payload.samples)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/assess")
async def assess(payload: AssessmentRequest, request: Request) -> dict[str, object]:
    try:
        return request.app.state.services.learning.assess(payload.features)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/feedback")
async def feedback(payload: FeedbackRequest, request: Request) -> dict[str, object]:
    try:
        return request.app.state.services.feedback.record(payload.detection_id, payload.verdict, payload.rule_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/versions")
async def versions(request: Request) -> list[dict[str, object]]:
    return [item.__dict__ for item in request.app.state.services.registry.list_versions()]
