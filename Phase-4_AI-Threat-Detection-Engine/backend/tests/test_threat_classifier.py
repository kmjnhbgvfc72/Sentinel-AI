from app.ai_engine.models import ThreatClassifier


def test_suspicious_login_classification():
    features = {"malware_indicator": 0, "ioc_reputation": 60, "failed_login_count": 10, "unknown_ip": 1, "data_access_log": 1, "frequency_ratio": 2}
    result = ThreatClassifier().predict(features)
    assert result["threat_type"] == "Suspicious Login"
    assert 0 <= result["confidence"] <= 100


def test_malware_indicator_classification():
    features = {"malware_indicator": 1, "ioc_reputation": 90, "failed_login_count": 0, "unknown_ip": 0, "data_access_log": 0, "frequency_ratio": 1}
    assert ThreatClassifier().predict(features)["threat_type"] == "Malware Indicator"
