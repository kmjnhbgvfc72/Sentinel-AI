from app.ai_engine.models import AnomalyDetector, BehaviorAnalyzer


def test_anomaly_detector_flags_hostile_pattern():
    features = {"failed_login_count": 12, "ioc_reputation": 92, "frequency_ratio": 8, "unknown_ip": 1, "new_device": 1, "location_changed": 0, "abnormal_time": 1, "malware_indicator": 0}
    result = AnomalyDetector().predict(features)
    assert result["anomaly"] is True
    assert result["anomaly_score"] >= 55


def test_behavior_analyzer_is_explainable():
    features = {"failed_login_count": 8, "new_device": 1, "location_changed": 1, "abnormal_time": 1, "frequency_ratio": 4, "unknown_ip": 1}
    flags = BehaviorAnalyzer().analyze(features)
    assert {"multiple_failed_logins", "new_device", "location_change", "unknown_ip"}.issubset(flags)
