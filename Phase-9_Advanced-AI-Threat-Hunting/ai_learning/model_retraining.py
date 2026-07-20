"""Guarded model retraining service."""
from datetime import datetime, timezone
from .self_learning import SelfLearningEngine


class ModelRetrainer:
    def __init__(self, engine: SelfLearningEngine) -> None:
        self.engine = engine

    def retrain(self, samples: list[list[float]]) -> dict[str, object]:
        version = self.engine.learn(samples)
        return {"status": "completed", "version_id": version.version_id, "metrics": version.metrics, "completed_at": datetime.now(timezone.utc).isoformat()}
