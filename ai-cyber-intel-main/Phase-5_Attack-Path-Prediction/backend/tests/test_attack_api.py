import pytest

pytestmark = pytest.mark.anyio

EVENT = {"event_id": "attack-test-001", "threat_type": "Suspicious Login", "severity": "critical", "confidence": 92, "risk_score": 90, "source_ip": "198.51.100.42", "user": "admin-account", "source_asset": "Web Server", "target_asset": "Database Server", "vulnerability": "CVE-2026-41001", "vulnerability_severity": "critical", "criticality": 95, "historical_incidents": 3}


async def test_analyze_and_read_endpoints(client):
    response = await client.post("/api/attack/analyze", json=EVENT)
    assert response.status_code == 200
    assert response.json()["data"]["paths"]
    for path in ("/api/attack/paths", "/api/attack/graph", "/api/risk/assets", "/api/recommendations"):
        result = await client.get(path)
        assert result.status_code == 200
        assert result.json()["data"]


async def test_validation_and_headers(client):
    response = await client.post("/api/attack/analyze", json={"event_id": "bad", "risk_score": 200})
    assert response.status_code == 422
    health = await client.get("/health")
    assert health.headers["x-content-type-options"] == "nosniff"
