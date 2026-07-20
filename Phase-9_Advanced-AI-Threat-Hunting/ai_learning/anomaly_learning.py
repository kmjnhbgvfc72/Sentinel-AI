"""Adaptive anomaly detection for numeric security-event features."""
from collections.abc import Sequence
import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyLearner:
    def __init__(self, contamination: float = 0.05) -> None:
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.trained = False

    def fit(self, samples: Sequence[Sequence[float]]) -> dict[str, float]:
        data = np.asarray(samples, dtype=float)
        if data.ndim != 2 or len(data) < 2:
            raise ValueError("at least two two-dimensional samples are required")
        self.model.fit(data)
        self.trained = True
        predictions = self.model.predict(data)
        return {"samples": float(len(data)), "anomaly_rate": float(np.mean(predictions == -1))}

    def score(self, sample: Sequence[float]) -> float:
        if not self.trained:
            raise RuntimeError("anomaly model has not been trained")
        raw = -float(self.model.decision_function(np.asarray([sample], dtype=float))[0])
        return round(max(0.0, min(1.0, 0.5 + raw)), 4)

    def is_anomaly(self, sample: Sequence[float], threshold: float = 0.5) -> bool:
        return self.score(sample) >= threshold
