from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response

from backend.config import Settings, get_settings
from backend.integrations.phase_client import PhaseClient, PhaseUnavailable
from backend.integrations.registry import build_registry

router = APIRouter(prefix="/phase", tags=["Phase gateway"])


@router.api_route("/{phase_number}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], include_in_schema=False)
async def proxy(phase_number: int, path: str, request: Request, settings: Settings = Depends(get_settings)) -> Response:
    phase = build_registry(settings).get(phase_number)
    if not phase:
        raise HTTPException(status_code=404, detail="Unknown phase")
    body = await request.body()
    try:
        upstream = await PhaseClient(phase, settings).request(
            request.method,
            f"/{path}",
            params=request.query_params.multi_items(),
            content=body or None,
            content_type=request.headers.get("content-type"),
        )
    except PhaseUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    headers = {}
    if upstream.headers.get("content-disposition"):
        headers["Content-Disposition"] = upstream.headers["content-disposition"]
    return Response(content=upstream.content, status_code=upstream.status_code, media_type=upstream.headers.get("content-type"), headers=headers)
