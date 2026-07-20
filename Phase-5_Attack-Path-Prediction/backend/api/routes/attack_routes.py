from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.schemas import AttackEvent, PathResponse
from config.attack_settings import get_settings
from database.attack_repository import AttackRepository, get_db
from services.attack_service import AttackService

router = APIRouter(prefix="/attack", tags=["Attack path analysis"])
settings = get_settings()


@router.post("/analyze")
async def analyze(event: AttackEvent, db: Session = Depends(get_db)) -> dict:
    return {"data": AttackService(db, settings).analyze(event).model_dump()}


@router.get("/paths")
async def paths(limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)) -> dict:
    data = [PathResponse.model_validate(item).model_dump(mode="json") for item in AttackRepository(db).paths(limit)]
    return {"data": data, "meta": {"total": len(data), "limit": limit}}


@router.get("/graph")
async def graph(db: Session = Depends(get_db)) -> dict:
    edges = AttackRepository(db).graph()
    return {"data": [{"id": edge.id, "source": edge.node_value, "target": edge.target_node, "relationship": edge.relationship, "node_type": edge.node_type} for edge in edges], "meta": {"total": len(edges)}}
