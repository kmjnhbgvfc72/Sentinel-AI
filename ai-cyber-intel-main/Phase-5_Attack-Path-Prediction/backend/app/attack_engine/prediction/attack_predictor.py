from pathlib import Path

from app.attack_engine.prediction.path_prediction_model import PathPredictionModel
from app.attack_engine.utils.graph_helpers import clamp, risk_level


class AttackPredictor:
    def __init__(self, model_path: Path | None = None):
        self.model = PathPredictionModel(model_path)

    def predict(self, graph, event: dict) -> list[dict]:
        source = event.get("source_ip") or event.get("threat_type", "Threat Event")
        destination = event.get("target_asset") or "Database Server"
        output = []
        for path in graph.paths(source, destination):
            base = event.get("risk_score", 0) * 0.55 + event.get("confidence", 50) * 0.2 + event.get("criticality", 50) * 0.15 + (15 if event.get("vulnerability_severity") in {"high", "critical"} else 0)
            # The shipped model is trained on path length and risk score.
            # Confidence is already incorporated into ``base`` and is kept
            # out of the model feature vector for schema compatibility.
            features = [len(path), event.get("risk_score", 0)]
            score = clamp(base + self.model.adjustment(features))
            output.append({"path": path, "risk_score": score, "risk_level": risk_level(score), "prediction": "possible attack path"})
        return output
