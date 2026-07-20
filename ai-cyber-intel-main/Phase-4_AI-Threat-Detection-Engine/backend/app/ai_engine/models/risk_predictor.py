from pathlib import Path

import joblib

from app.ai_engine.training.feature_engineering import feature_frame
from app.ai_engine.utils import clamp, severity_for_score


class RiskPredictor:
    def __init__(self, model_path: Path | None = None):
        self.model = joblib.load(model_path) if model_path and model_path.is_file() else None

    def predict(self, features: dict[str, float], anomaly_score: float, confidence: float) -> dict:
        if self.model:
            score = clamp(float(self.model.predict(feature_frame([features]))[0]))
        else:
            score = clamp(features["ioc_reputation"] * 0.25 + features["vulnerability_score"] * 5 + features["failed_login_count"] * 2 + features["severity_value"] * 5 + anomaly_score * 0.15 + confidence * 0.1 + features["malware_indicator"] * 10)
        return {"risk_score": score, "severity": severity_for_score(score)}
