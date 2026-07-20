from contextlib import asynccontextmanager
from datetime import UTC, datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.soar_settings import get_settings
from database.soar_repository import initialize_database, SessionLocal
from app.playbooks.workflow_engine import ensure_playbooks
from api.routes.incident_routes import router as incident_router
from api.routes.playbook_routes import router as playbook_router
from api.routes.response_routes import router as response_router
from api.routes.notification_routes import router as notification_router
from api.routes.report_routes import router as report_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_):
    initialize_database()
    with SessionLocal() as session:
        ensure_playbooks(session)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.now(UTC),
    }


app.include_router(incident_router, prefix="/api")
app.include_router(playbook_router, prefix="/api")
app.include_router(response_router, prefix="/api")
app.include_router(notification_router, prefix="/api")
app.include_router(report_router, prefix="/api")
