from fastapi import APIRouter

from app.api.controllers.system_controller import get_system_health

router = APIRouter(tags=["System"])


@router.get("/health", summary="Check API health")
def health_check() -> dict[str, str]:
    return get_system_health()
