from app.ai_engine.models import RiskPredictor


def test_risk_is_bounded_and_critical():
    features = {"ioc_reputation": 95, "vulnerability_score": 9, "failed_login_count": 12, "severity_value": 4, "malware_indicator": 1}
    result = RiskPredictor().predict(features, anomaly_score=95, confidence=95)
    assert 0 <= result["risk_score"] <= 100
    assert result["severity"] == "critical"
