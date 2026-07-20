from pathlib import Path

import joblib

from app.ai_engine.training.feature_engineering import feature_frame
from app.ai_engine.utils import clamp


class AnomalyDetector:
    def __init__(self, model_path: Path | None = None):
        self.model = joblib.load(model_path) if model_path and model_path.is_file() else None

    def predict(self, features: dict[str, float]) -> dict:
        if self.model:
            frame = feature_frame([features])
            anomaly = bool(self.model.predict(frame)[0] == -1)
            score = clamp(-float(self.model.decision_function(frame)[0]) * 100 + 50)
        else:
            score = clamp(features["failed_login_count"] * 5 + features["ioc_reputation"] * 0.35 + features["frequency_ratio"] * 4 + sum(features[key] for key in ("unknown_ip", "new_device", "location_changed", "abnormal_time", "malware_indicator")) * 10)
            anomaly = score >= 55
        return {"anomaly": anomaly, "anomaly_score": score}
