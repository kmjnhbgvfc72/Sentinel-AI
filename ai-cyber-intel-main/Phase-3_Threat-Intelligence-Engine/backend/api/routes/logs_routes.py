from math import ceil

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ActivityLogResponse, Severity
from app.threat_intelligence.services import IntelligenceService

router = APIRouter(tags=["Security logs"])


@router.get("/logs")
async def list_logs(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), risk_level: Severity | None = None, db: Session = Depends(get_db)) -> dict:
    records, total = IntelligenceService(db).list_logs(page=page, page_size=page_size, risk_level=risk_level.value if risk_level else None)
    return {"data": [ActivityLogResponse.model_validate(item).model_dump(mode="json") for item in records], "meta": {"page": page, "page_size": page_size, "total": total, "pages": max(1, ceil(total / page_size))}}
