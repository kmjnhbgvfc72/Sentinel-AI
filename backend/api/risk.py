from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.api.threats import ThreatResponse
from backend.database import get_db
from backend.models import User
from backend.services.risk_service import RiskCalculationService

router = APIRouter(prefix="/risk", tags=["Authentication risk"])


class RiskResponse(BaseModel):
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    risk_score: int
    events: list[ThreatResponse]
    distribution: dict[Literal["LOW", "MEDIUM", "HIGH"], int]


@router.get("", response_model=RiskResponse)
def current_risk(_: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    return RiskCalculationService(db).current_risk()
