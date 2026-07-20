from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.feed_routes import router as feed_router
from api.routes.intelligence_routes import router as intelligence_router
from api.routes.ioc_routes import router as ioc_router
from api.routes.reputation_routes import router as reputation_router
from app.errors import ServiceError
from app.logging_config import configure_logging
from app.seed import seed_demo_data
from config.settings import get_settings
from database.connection import SessionLocal, initialize_database
from services.scheduler import FeedScheduler

settings = get_settings()
configure_logging(settings.log_level)
scheduler = FeedScheduler(settings)


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    if settings.demo_data_enabled:
        with SessionLocal() as session:
            seed_demo_data(session)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title=settings.app_name, version=settings.app_version, description="Defensive IOC, feed, reputation, and cross-phase correlation platform", lifespan=lifespan)


class SecurityHeadersMiddleware:
    def __init__(self, wrapped_app):
        self.app = wrapped_app

    async def __call__(self, scope, receive, send):
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                message["headers"] = list(message.get("headers", [])) + [(b"x-content-type-options", b"nosniff"), (b"x-frame-options", b"DENY"), (b"referrer-policy", b"no-referrer"), (b"content-security-policy", b"default-src 'none'; frame-ancestors 'none'")]
            await send(message)
        await self.app(scope, receive, send_with_headers)


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=False, allow_methods=["GET", "POST", "DELETE"], allow_headers=["Accept", "Content-Type"])


@app.exception_handler(ServiceError)
async def service_error(_: Request, exc: ServiceError):
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": exc.code, "message": exc.message}})


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError):
    fields = [{"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"]} for error in exc.errors()]
    return JSONResponse(status_code=422, content={"error": {"code": "validation_error", "message": "Request validation failed", "fields": fields}})


@app.get("/health", tags=["System"])
async def health():
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version, "timestamp": datetime.now(UTC)}


for route in (feed_router, ioc_router, reputation_router, intelligence_router):
    app.include_router(route, prefix="/api")
