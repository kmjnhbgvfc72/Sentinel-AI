"""IOC and intelligence REST routes."""
from typing import Any
from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/intelligence", tags=["Threat Intelligence"])


class IOCRequest(BaseModel):
    type: str
    value: str = Field(min_length=1, max_length=2048)
    confidence: float = Field(default=0.5, ge=0, le=1)
    source: str = Field(default="manual", max_length=200)
    tags: list[str] = Field(default_factory=list, max_length=50)


class EnrichmentRequest(BaseModel):
    confidence: float = Field(default=0.5, ge=0, le=1)
    sightings: int = Field(default=1, ge=0)
    behaviors: list[str] = Field(default_factory=list)
    attributes: dict[str, Any] = Field(default_factory=dict)


@router.post("/iocs", status_code=status.HTTP_201_CREATED)
async def create_ioc(payload: IOCRequest, request: Request) -> dict[str, object]:
    try:
        return request.app.state.services.iocs.upsert(
            payload.type,
            payload.value,
            payload.confidence,
            payload.source,
            payload.tags,
        ).__dict__
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/iocs")
async def list_iocs(request: Request, query: str = "", ioc_type: str | None = None) -> list[dict[str, object]]:
    return request.app.state.services.iocs.search(query, ioc_type)


@router.post("/enrich")
async def enrich(payload: EnrichmentRequest, request: Request) -> dict[str, object]:
    return request.app.state.services.intelligence.enrich({**payload.attributes, **payload.model_dump(exclude={"attributes"})})
