import logging
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from ai_production.model_loader import ModelLoader
from ai_production.prediction_engine import PredictionEngine
from api.alert_api import router as alert_router
from api.auth_api import router as auth_router
from api.response_api import router as response_router
from api.threat_api import prediction_router, router as threat_router
from config import get_settings
from database.connection import Base, engine
from monitoring.health_check import system_health

settings = get_settings()
REQUESTS = Counter("soc_http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("soc_http_request_duration_seconds", "HTTP latency", ["method", "path"])
loader = ModelLoader(settings.model_path)
predictor = PredictionEngine(loader)


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.validate_production()
    Base.metadata.create_all(engine)
    loader.load()
    yield
    engine.dispose()


app = FastAPI(title="Enterprise AI Security Operations Center", version="8.0.0", docs_url="/api/docs", openapi_url="/api/openapi.json", lifespan=lifespan)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=False, allow_methods=["GET", "POST", "PATCH"], allow_headers=["Authorization", "Content-Type", "X-Request-ID"])


@app.middleware("http")
async def observability_and_security(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))[:128]
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logging.exception("Unhandled request error request_id=%s", request_id)
        response = JSONResponse({"detail": "Internal server error", "request_id": request_id}, 500)
    path = request.scope.get("route").path if request.scope.get("route") else "unmatched"
    REQUESTS.labels(request.method, path, response.status_code).inc()
    LATENCY.labels(request.method, path).observe(time.perf_counter() - started)
    response.headers.update({"X-Request-ID": request_id, "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "no-referrer", "Permissions-Policy": "camera=(), microphone=(), geolocation=()", "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'"})
    return response


@app.get("/health/live", tags=["Health"])
def live(): return {"status": "alive"}


@app.get("/health/ready", tags=["Health"])
def ready():
    health = system_health(loader.loaded)
    return JSONResponse(health, status_code=200 if health["database"] else 503)


@app.get("/metrics", include_in_schema=False)
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


for router in (auth_router, threat_router, prediction_router(predictor), alert_router, response_router):
    app.include_router(router, prefix="/api/v1")

