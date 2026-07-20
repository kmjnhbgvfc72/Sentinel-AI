from math import ceil
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import IndicatorResponse
from app.threat_intelligence.services import IntelligenceService

router = APIRouter(tags=["Indicators"])


@router.get("/indicators")
async def list_indicators(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), indicator_type: Literal["ip", "domain", "sha256", "sha1", "md5"] | None = None, db: Session = Depends(get_db)) -> dict:
    records, total = IntelligenceService(db).list_indicators(page=page, page_size=page_size, indicator_type=indicator_type)
    return {"data": [IndicatorResponse.model_validate(item).model_dump(mode="json") for item in records], "meta": {"page": page, "page_size": page_size, "total": total, "pages": max(1, ceil(total / page_size))}}
