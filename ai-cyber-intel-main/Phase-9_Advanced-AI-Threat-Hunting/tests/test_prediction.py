"""Prediction tests."""
from prediction.attack_forecast import AttackForecaster
from prediction.attack_path_predictor import AttackPathPredictor
from prediction.risk_forecast import RiskForecaster


def test_attack_forecast_is_bounded() -> None:
    result = AttackForecaster().forecast({"threat_velocity": 1, "asset_exposure": 0.8, "vulnerability_score": 0.9, "adversary_activity": 1})
    assert 0 <= result["attack_probability"] <= 1
    assert result["risk_band"] in {"low", "medium", "high", "critical"}


def test_path_and_risk_prediction() -> None:
    paths = AttackPathPredictor().predict([{"source": "internet", "target": "web", "probability": 0.8}, {"source": "web", "target": "db", "probability": 0.5}], "internet", ["db"])
    risk = RiskForecaster().forecast([{"asset": "db", "likelihood": 0.8, "impact": 9, "control_effectiveness": 0.5}])
    assert paths[0]["path"] == ["internet", "web", "db"]
    assert risk["aggregate_risk"] == 36.0
