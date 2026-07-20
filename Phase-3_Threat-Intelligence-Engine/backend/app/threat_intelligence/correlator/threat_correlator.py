from typing import Any

from app.threat_intelligence.utils import clamp_score, risk_level_for_score


def correlate_threat(*, indicator: dict[str, Any] | None, failed_auth_events: int, vulnerability: dict[str, Any] | None, suspicious_log: dict[str, Any] | None = None) -> dict[str, Any]:
    indicator_score = float((indicator or {}).get("reputation_score") or 0)
    confidence = float((indicator or {}).get("confidence_score") or 0)
    auth_score = min(max(failed_auth_events, 0) * 4, 30)
    vulnerability_score = {"critical": 30, "high": 22, "medium": 12, "low": 4}.get(str((vulnerability or {}).get("severity", "")).lower(), 0)
    log_score = min(float((suspicious_log or {}).get("risk_score") or 0) * 0.2, 20)
    risk_score = clamp_score(indicator_score * 0.35 + auth_score + vulnerability_score + log_score)
    severity = risk_level_for_score(risk_score)
    return {"name": "High Risk Attack Indicator" if risk_score >= 70 else "Correlated Security Indicator", "risk_score": risk_score, "risk_category": "high-risk correlated activity" if risk_score >= 70 else "review required" if risk_score >= 40 else "low risk", "severity": severity, "threat_confidence": clamp_score(confidence * 0.55 + (20 if failed_auth_events >= 5 else 0) + (15 if vulnerability else 0) + (10 if suspicious_log else 0)), "evidence": {"indicator_reputation": indicator_score, "failed_auth_events": failed_auth_events, "vulnerability_severity": (vulnerability or {}).get("severity"), "log_risk_score": (suspicious_log or {}).get("risk_score")}}
