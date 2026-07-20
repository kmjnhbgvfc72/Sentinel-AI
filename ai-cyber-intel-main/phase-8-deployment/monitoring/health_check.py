import time
import psutil
from sqlalchemy import text
from database.connection import engine

STARTED = time.monotonic()


def system_health(model_loaded: bool) -> dict:
    checks = {"database": False, "model": model_loaded, "cpu_percent": psutil.cpu_percent(), "memory_percent": psutil.virtual_memory().percent, "uptime_seconds": round(time.monotonic() - STARTED)}
    try:
        with engine.connect() as conn: conn.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception: pass
    checks["status"] = "healthy" if checks["database"] else "degraded"
    return checks

