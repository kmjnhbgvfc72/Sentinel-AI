from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.alert_routes import router as alert_router
from api.asset_routes import router as asset_router
from api.dashboard_routes import router as dashboard_router
from api.report_routes import router as report_router
from api.threat_routes import router as threat_router
from config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version, description="Defensive SOC dashboard API")


class SecurityHeadersMiddleware:
    """Pure ASGI middleware avoids buffering response bodies."""

    def __init__(self, wrapped_app):
        self.app = wrapped_app

    async def __call__(self, scope, receive, send):
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"x-content-type-options", b"nosniff"),
                    (b"x-frame-options", b"DENY"),
                    (b"referrer-policy", b"no-referrer"),
                    (b"permissions-policy", b"camera=(), microphone=(), geolocation=()"),
                ])
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=False, allow_methods=["GET", "PATCH"], allow_headers=["Accept", "Content-Type"])


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    fields = [{"field": ".".join(str(part) for part in error["loc"]), "message": error["msg"]} for error in exc.errors()]
    return JSONResponse(status_code=422, content={"error": {"code": "validation_error", "message": "Request validation failed", "fields": fields}})


@app.exception_handler(Exception)
async def unexpected_error(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"error": {"code": "internal_error", "message": "The service could not process the request"}})


def health_payload() -> dict:
    return {"status": "healthy", "service": settings.app_name, "version": settings.app_version, "timestamp": datetime.now(UTC)}


@app.get("/health", tags=["System"])
async def health() -> dict:
    return health_payload()


@app.get("/api/health", tags=["System"])
async def api_health() -> dict:
    return health_payload()


app.include_router(dashboard_router, prefix="/api")
app.include_router(threat_router, prefix="/api")
app.include_router(alert_router, prefix="/api")
app.include_router(asset_router, prefix="/api")
app.include_router(report_router, prefix="/api")
