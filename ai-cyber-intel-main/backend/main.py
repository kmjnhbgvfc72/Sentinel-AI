from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.auth import router as auth_router
from backend.api.gateway import router as gateway_router
from backend.api.logs import router as logs_router
from backend.api.notifications import router as notifications_router
from backend.api.pipeline import router as pipeline_router
from backend.api.reports import router as reports_router
from backend.api.system import router as system_router
from backend.config import get_settings
from backend.database import SessionLocal, initialize_database
from backend.services.auth_service import AuthService

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    with SessionLocal() as db:
        AuthService(db, settings.auth_token_ttl_minutes).bootstrap_admin(
            settings.bootstrap_admin_username,
            settings.bootstrap_admin_email,
            settings.bootstrap_admin_password,
        )
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, description="Central gateway and orchestration API for Phases 1-9", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=False, allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"], allow_headers=["Authorization", "Content-Type", "X-API-Key", "X-Request-ID"])


@app.get("/health", tags=["Central system"])
def root_health() -> dict:
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version}


for router in (system_router, pipeline_router, gateway_router):
    app.include_router(router, prefix="/api/v1")

for router in (auth_router, logs_router, notifications_router, reports_router):
    app.include_router(router, prefix="/api")
