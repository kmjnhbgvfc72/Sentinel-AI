from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.attack_routes import router as attack_router
from api.routes.recommendation_routes import router as recommendation_router
from api.routes.risk_routes import router as risk_router
from config.attack_settings import get_settings
from database.attack_repository import SessionLocal, initialize_database
from services.attack_service import AttackService
from app.schemas import AttackEvent

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    if settings.demo_data_enabled:
        with SessionLocal() as session:
            AttackService(session, settings).analyze(AttackEvent(event_id="demo-attack-001", threat_type="Suspicious Login", severity="critical", confidence=92, risk_score=90, source_ip="198.51.100.42", user="admin-account", source_asset="Web Server", target_asset="Database Server", vulnerability="CVE-2026-41001", vulnerability_severity="critical", criticality=95, historical_incidents=3))
    if settings.auto_analyze_phase4:
        with SessionLocal() as session:
            service = AttackService(session, settings)
            for event in await service.fetch_phase4_events():
                service.analyze(event)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, description="Defensive attack path prediction and asset risk analysis", lifespan=lifespan)


class SecurityHeadersMiddleware:
    def __init__(self, wrapped_app):
        self.app = wrapped_app

    async def __call__(self, scope, receive, send):
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                message["headers"] = list(message.get("headers", [])) + [(b"x-content-type-options", b"nosniff"), (b"x-frame-options", b"DENY"), (b"referrer-policy", b"no-referrer")]
            await send(message)
        await self.app(scope, receive, send_with_headers)


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Accept", "Content-Type"])


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    fields = [{"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"]} for error in exc.errors()]
    return JSONResponse(status_code=422, content={"error": {"code": "validation_error", "message": "Request validation failed", "fields": fields}})


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version, "timestamp": datetime.now(UTC)}


app.include_router(attack_router, prefix="/api")
app.include_router(risk_router, prefix="/api")
app.include_router(recommendation_router, prefix="/api")
