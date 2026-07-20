"""Threat-hunting tests."""
from threat_hunting.hunter import ThreatHunter
from threat_hunting.ioc_engine import IOCEngine
from threat_intelligence.ioc_database import IOCDatabase


def test_hunter_correlates_known_ioc_and_behavior() -> None:
    database = IOCDatabase()
    database.upsert("domain", "malicious.example", 0.9, "test")
    result = ThreatHunter(IOCEngine(database)).hunt({"id": "evt-1", "text": "DNS lookup malicious.example", "behaviors": ["credential_access", "lateral_movement"]})
    assert result["ioc_matches"][0]["known"]
    assert result["attack_patterns"][0]["pattern"] == "credential-to-lateral-movement"


def test_ioc_validation_rejects_bad_ip() -> None:
    database = IOCDatabase()
    try:
        database.upsert("ipv4", "999.1.1.1")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid IP was accepted")
