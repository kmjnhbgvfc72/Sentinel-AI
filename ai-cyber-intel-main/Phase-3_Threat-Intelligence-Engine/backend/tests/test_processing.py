import pytest

from app.threat_intelligence.collectors.domain_reputation_collector import DomainReputationCollector
from app.threat_intelligence.collectors.ip_reputation_collector import IPReputationCollector
from app.threat_intelligence.collectors.log_collector import LogCollector
from app.threat_intelligence.collectors.malware_feed_collector import MalwareFeedCollector
from app.threat_intelligence.correlator import correlate_threat
from app.threat_intelligence.parsers.feed_parser import parse_feed_record


def test_high_risk_correlation():
    result = correlate_threat(indicator={"reputation_score": 95, "confidence_score": 90}, failed_auth_events=10, vulnerability={"severity": "critical"})
    assert result["severity"] == "critical"


def test_collectors_validate_observables():
    assert IPReputationCollector().normalize({"ip_address": "198.51.100.5", "reputation_score": 90})["status"] == "malicious"
    assert DomainReputationCollector().normalize({"domain": "Example.Test"})["value"] == "example.test"
    assert MalwareFeedCollector().normalize({"hash": "a" * 64})["hash_type"] == "sha256"
    with pytest.raises(ValueError):
        DomainReputationCollector().normalize({"domain": "invalid domain"})


def test_log_redaction_and_feed_validation():
    log = LogCollector().collect([{"log_type": "authentication", "event_type": "suspicious_login", "failed_login_count": 10, "unknown_ip": True, "password": "never-store"}])[0]
    assert log["risk_level"] == "critical"
    assert "password" not in log["details"]
    with pytest.raises(ValueError):
        parse_feed_record({"name": "incomplete"})
