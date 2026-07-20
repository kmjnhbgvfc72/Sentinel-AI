from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas import AssetResponse
from database.attack_repository import AttackRepository, get_db

router = APIRouter(prefix="/risk", tags=["Asset risk"])


@router.get("/assets")
async def assets(limit: int = Query(100, ge=1, le=200), db: Session = Depends(get_db)) -> dict:
    data = [AssetResponse.model_validate(item).model_dump(mode="json") for item in AttackRepository(db).assets(limit)]
    return {"data": data, "meta": {"total": len(data), "limit": limit}}
