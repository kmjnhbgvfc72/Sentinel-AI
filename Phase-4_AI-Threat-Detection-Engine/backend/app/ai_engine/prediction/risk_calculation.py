from app.ai_engine.utils import clamp, severity_for_score


def calculate_risk(*, model_score: float, anomaly_score: float, behavior_flags: int) -> dict:
    score = clamp(model_score * 0.75 + anomaly_score * 0.2 + min(behavior_flags * 2, 10) * 0.05)
    return {"risk_score": score, "severity": severity_for_score(score)}
