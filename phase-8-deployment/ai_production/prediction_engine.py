from datetime import UTC, datetime, timedelta
import numpy as np
from ai_production.model_loader import ModelLoader
from ai_production.risk_scoring import RiskFactors, calculate_risk, risk_level


class PredictionEngine:
    def __init__(self, loader: ModelLoader): self.loader = loader

    def predict(self, features: RiskFactors, context: dict | None = None) -> dict:
        fallback = calculate_risk(features) / 100
        model = self.loader.load()
        vector = np.array([[features.anomaly_score, features.asset_criticality, features.threat_confidence, features.exposure]])
        if model is not None:
            probability = float(model.predict_proba(vector)[0][-1]) if hasattr(model, "predict_proba") else float(model.predict(vector)[0])
            probability = max(0.0, min(1.0, probability))
        else:
            probability = fallback
        score = round(probability * 100, 2)
        paths = self._attack_paths(features, context or {})
        return {"probability": round(probability, 4), "risk_score": score, "risk_level": risk_level(score), "attack_paths": paths,
                "warning_horizon": (datetime.now(UTC) + timedelta(hours=6 if score >= 65 else 24)).isoformat(),
                "model_mode": "trained" if model is not None else "deterministic-fallback",
                "recommended_actions": self._actions(score, paths)}

    @staticmethod
    def _attack_paths(f: RiskFactors, context: dict) -> list[dict]:
        paths = []
        if f.exposure >= .5: paths.append({"path": ["internet", "edge-service", context.get("asset", "target")], "confidence": round(f.exposure * f.threat_confidence, 3)})
        if f.anomaly_score >= .6: paths.append({"path": ["compromised-identity", "internal-service", context.get("asset", "target")], "confidence": round(f.anomaly_score * .8, 3)})
        return sorted(paths, key=lambda item: item["confidence"], reverse=True)

    @staticmethod
    def _actions(score: float, paths: list[dict]) -> list[str]:
        actions = ["Increase telemetry collection", "Validate indicators with threat intelligence"]
        if score >= 65: actions += ["Require analyst review", "Restrict suspicious identities"]
        if score >= 85: actions += ["Isolate affected endpoint", "Block confirmed malicious infrastructure"]
        return actions

