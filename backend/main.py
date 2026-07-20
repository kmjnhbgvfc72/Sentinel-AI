from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from backend.api.auth import router as auth_router
from backend.api.alerts import router as alerts_router
from backend.api.gateway import router as gateway_router
from backend.api.logs import router as logs_router
from backend.api.operations import router as operations_router
from backend.api.risk import router as risk_router
from backend.api.pipeline import router as pipeline_router
from backend.api.system import router as system_router
from backend.api.threats import router as threats_router
from backend.config import get_settings
from backend.database import SessionLocal, initialize_database
from backend.services.auth_service import AuthService

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.database_ready = False
    try:
        initialize_database()
        with SessionLocal() as db:
            AuthService(db, settings.auth_token_ttl_minutes).bootstrap_admin(
                settings.bootstrap_admin_username,
                settings.bootstrap_admin_email,
                settings.bootstrap_admin_password,
            )
        application.state.database_ready = True
    except OperationalError as exc:
        logger.error("Central database is unavailable; API started in degraded mode: %s", exc.orig)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, description="Central gateway and orchestration API for Phases 1-9", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=False, allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"], allow_headers=["Authorization", "Content-Type", "X-API-Key", "X-Request-ID"])


@app.get("/health", tags=["Central system"])
def root_health() -> dict:
    database_ready = getattr(app.state, "database_ready", False)
    return {"status": "healthy" if database_ready else "degraded", "database": "ready" if database_ready else "unavailable", "service": settings.app_name, "version": settings.app_version}


for router in (system_router, pipeline_router, gateway_router):
    app.include_router(router, prefix="/api/v1")

for router in (auth_router, logs_router, alerts_router, threats_router, risk_router, operations_router):
    app.include_router(router, prefix="/api")
