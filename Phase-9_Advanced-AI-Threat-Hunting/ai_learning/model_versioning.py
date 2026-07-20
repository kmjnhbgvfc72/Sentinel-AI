"""Immutable model-version registry."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4


@dataclass(frozen=True)
class ModelVersion:
    version_id: str
    model_name: str
    metrics: dict[str, float]
    created_at: str
    active: bool = True


class ModelRegistry:
    """Thread-safe registry suitable for replacement by an MLflow adapter."""

    def __init__(self) -> None:
        self._versions: list[ModelVersion] = []
        self._lock = RLock()

    def register(self, model_name: str, metrics: dict[str, float]) -> ModelVersion:
        with self._lock:
            self._versions = [ModelVersion(**{**asdict(v), "active": False}) for v in self._versions]
            version = ModelVersion(str(uuid4()), model_name, metrics, datetime.now(timezone.utc).isoformat())
            self._versions.append(version)
            return version

    def list_versions(self) -> list[ModelVersion]:
        with self._lock:
            return list(self._versions)

    def active(self) -> ModelVersion | None:
        return next((v for v in reversed(self.list_versions()) if v.active), None)
