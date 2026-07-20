from math import ceil

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import Severity, ThreatResponse
from app.threat_intelligence.services import ThreatService

router = APIRouter(tags=["Threat intelligence"])


@router.get("/threats")
async def list_threats(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), severity: Severity | None = None, threat_type: str | None = Query(None, max_length=100), db: Session = Depends(get_db)) -> dict:
    records, total = ThreatService(db).list_threats(page=page, page_size=page_size, severity=severity.value if severity else None, threat_type=threat_type)
    return {"data": [ThreatResponse.model_validate(item).model_dump(mode="json") for item in records], "meta": {"page": page, "page_size": page_size, "total": total, "pages": max(1, ceil(total / page_size))}}


@router.get("/threat-statistics")
async def statistics(db: Session = Depends(get_db)) -> dict:
    return {"data": ThreatService(db).statistics()}
