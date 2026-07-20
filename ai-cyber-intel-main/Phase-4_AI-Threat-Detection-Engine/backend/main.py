from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.ai_detection_routes import router as ai_router
from app.seed import seed_demo_data
from config.ai_settings import get_settings
from database.ai_repository import SessionLocal, initialize_database
from services.ai_service import AIService

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    if settings.demo_data_enabled:
        seed_demo_data(settings)
    if settings.auto_analyze_phase3:
        with SessionLocal() as session:
            service = AIService(session, settings)
            for event in await service.fetch_phase3_events():
                service.analyze(event)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, description="Defensive AI anomaly detection, threat classification, and risk analysis", lifespan=lifespan)


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


@app.get("/health", tags=["System"])
async def health() -> dict:
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version, "timestamp": datetime.now(UTC)}


app.include_router(ai_router, prefix="/api")
