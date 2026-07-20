from pathlib import Path

from app.ai_engine.models import AnomalyDetector, BehaviorAnalyzer, RiskPredictor, ThreatClassifier
from app.ai_engine.preprocessing import DataProcessor
from app.schemas import AnalysisResponse, SecurityEvent


class ThreatPredictionEngine:
    def __init__(self, model_directory: Path, model_version: str = "4.0.0"):
        self.processor = DataProcessor()
        self.anomaly = AnomalyDetector(model_directory / "anomaly_model.pkl")
        self.classifier = ThreatClassifier(model_directory / "threat_classifier.pkl")
        self.risk = RiskPredictor(model_directory / "risk_prediction_model.pkl")
        self.behavior = BehaviorAnalyzer()
        self.model_version = model_version

    def analyze(self, event: SecurityEvent, alert_threshold: float) -> tuple[AnalysisResponse, dict[str, float]]:
        features = self.processor.process(event)
        anomaly = self.anomaly.predict(features)
        classification = self.classifier.predict(features)
        risk = self.risk.predict(features, anomaly["anomaly_score"], classification["confidence"])
        flags = self.behavior.analyze(features)
        response = AnalysisResponse(event_id=event.event_id, anomaly=anomaly["anomaly"], anomaly_score=anomaly["anomaly_score"], threat_type=classification["threat_type"], confidence=classification["confidence"], risk_score=risk["risk_score"], severity=risk["severity"], behavior_flags=flags, alert_generated=risk["risk_score"] >= alert_threshold, model_version=self.model_version)
        return response, features
