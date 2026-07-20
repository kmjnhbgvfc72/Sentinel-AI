from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas import RecommendationResponse
from database.attack_repository import AttackRepository, get_db

router = APIRouter(tags=["Recommendations"])


@router.get("/recommendations")
async def recommendations(limit: int = Query(100, ge=1, le=200), db: Session = Depends(get_db)) -> dict:
    data = [RecommendationResponse.model_validate(item).model_dump(mode="json") for item in AttackRepository(db).recommendations(limit)]
    return {"data": data, "meta": {"total": len(data), "limit": limit}}
