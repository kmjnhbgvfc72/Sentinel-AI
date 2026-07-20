"""Orchestration for continuous learning from historical events."""
from .anomaly_learning import AnomalyLearner
from .feedback_engine import FeedbackEngine
from .model_versioning import ModelRegistry, ModelVersion


class SelfLearningEngine:
    def __init__(self, anomaly: AnomalyLearner | None = None, feedback: FeedbackEngine | None = None, registry: ModelRegistry | None = None) -> None:
        self.anomaly = anomaly or AnomalyLearner()
        self.feedback = feedback or FeedbackEngine()
        self.registry = registry or ModelRegistry()

    def learn(self, samples: list[list[float]]) -> ModelVersion:
        metrics = self.anomaly.fit(samples)
        metrics["analyst_precision"] = float(self.feedback.quality()["precision"])
        return self.registry.register("isolation-forest", metrics)

    def assess(self, features: list[float]) -> dict[str, object]:
        score = self.anomaly.score(features)
        return {"anomaly_score": score, "anomaly": score >= 0.5, "model_version": getattr(self.registry.active(), "version_id", None)}
