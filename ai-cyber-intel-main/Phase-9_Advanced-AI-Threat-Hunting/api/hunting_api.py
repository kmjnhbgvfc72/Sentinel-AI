"""Threat hunting REST routes."""
from typing import Any
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/hunting", tags=["Threat Hunting"])


class HuntRequest(BaseModel):
    id: str | None = None
    text: str = Field(default="", max_length=100_000)
    behaviors: list[str] = Field(default_factory=list, max_length=100)
    fields: dict[str, Any] = Field(default_factory=dict)


@router.post("/search")
async def hunt(payload: HuntRequest, request: Request) -> dict[str, object]:
    event = {**payload.fields, "id": payload.id, "text": payload.text, "behaviors": payload.behaviors}
    return request.app.state.services.hunter.hunt(event)


@router.get("/iocs")
async def search_iocs(request: Request, query: str = "", ioc_type: str | None = None) -> list[dict[str, object]]:
    return request.app.state.services.iocs.search(query, ioc_type)
