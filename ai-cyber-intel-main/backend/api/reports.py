import json
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.api.auth import current_user
from backend.database import get_db
from backend.models import Report, User
from backend.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Security reports"])
ReportType = Literal["daily_security", "threat_analysis", "incident"]


class ReportGenerateRequest(BaseModel): report_type: ReportType


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; report_type: str; generated_by: str; summary: dict; created_at: datetime


def serialize(item: Report) -> ReportResponse:
    return ReportResponse(id=item.id, report_type=item.report_type, generated_by=item.generated_by, summary=json.loads(item.summary), created_at=item.created_at)


@router.get("", response_model=list[ReportResponse])
def list_reports(_: User = Depends(current_user), db: Session = Depends(get_db)) -> list[ReportResponse]:
    return [serialize(item) for item in ReportService(db).list()]


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(payload: ReportGenerateRequest, user: User = Depends(current_user), db: Session = Depends(get_db)) -> ReportResponse:
    return serialize(ReportService(db).generate(payload.report_type, user.username))


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, _: User = Depends(current_user), db: Session = Depends(get_db)) -> ReportResponse:
    item = ReportService(db).get(report_id)
    if not item: raise HTTPException(status_code=404, detail="Report not found")
    return serialize(item)
