from pathlib import Path

import joblib

from app.ai_engine.training.feature_engineering import feature_frame
from app.ai_engine.utils import clamp


class ThreatClassifier:
    def __init__(self, model_path: Path | None = None):
        self.model = joblib.load(model_path) if model_path and model_path.is_file() else None

    def predict(self, features: dict[str, float]) -> dict:
        if self.model:
            frame = feature_frame([features])
            label = str(self.model.predict(frame)[0])
            confidence = clamp(max(self.model.predict_proba(frame)[0]) * 100)
            return {"threat_type": label, "confidence": confidence}
        if features["malware_indicator"] or features["ioc_reputation"] >= 85:
            label, confidence = "Malware Indicator", max(80, features["ioc_reputation"])
        elif features["failed_login_count"] >= 5 or features["unknown_ip"]:
            label, confidence = "Suspicious Login", min(98, 65 + features["failed_login_count"] * 3)
        elif features["data_access_log"] >= 50:
            label, confidence = "Data Access Anomaly", 82
        elif features["frequency_ratio"] >= 5:
            label, confidence = "Bot Activity", 78
        else:
            label, confidence = "Unknown Threat", 55
        return {"threat_type": label, "confidence": clamp(confidence)}
