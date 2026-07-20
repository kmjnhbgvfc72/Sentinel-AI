from typing import Any

SENSITIVE_FIELDS = {"password", "passwd", "secret", "token", "access_token", "refresh_token", "authorization", "cookie", "credential", "api_key"}


def clamp_score(value: float) -> float:
    return round(max(0.0, min(float(value), 100.0)), 1)


def risk_level_for_score(score: float) -> str:
    return "critical" if score >= 85 else "high" if score >= 70 else "medium" if score >= 40 else "low"


def sanitize_log_details(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): sanitize_log_details(item) for key, item in value.items() if str(key).lower() not in SENSITIVE_FIELDS}
    if isinstance(value, list):
        return [sanitize_log_details(item) for item in value[:100]]
    return value[:1000] if isinstance(value, str) else value
