from app.schemas import SecurityEvent


class DataProcessor:
    """Converts validated events into a stable, credential-free feature record."""

    def process(self, event: SecurityEvent) -> dict[str, float]:
        baseline = max(event.historical_average, 1.0)
        frequency_ratio = min(event.activity_frequency / baseline, 20.0)
        severity_value = {"low": 1, "medium": 2, "high": 3, "critical": 4}[event.severity]
        return {
            "failed_login_count": float(event.failed_login_count),
            "ioc_reputation": event.ioc_reputation,
            "vulnerability_score": event.vulnerability_score,
            "frequency_ratio": frequency_ratio,
            "unknown_ip": float(event.unknown_ip),
            "new_device": float(event.new_device),
            "location_changed": float(event.location_changed),
            "abnormal_time": float(event.abnormal_time),
            "malware_indicator": float(event.malware_indicator),
            "severity_value": float(severity_value),
            "data_access_log": min(event.data_access_volume / 1_000_000, 1000.0),
        }
