import pytest

pytestmark = pytest.mark.anyio

EVENT = {"event_id": "test-event-001", "event_type": "authentication", "severity": "critical", "failed_login_count": 10, "ioc_reputation": 90, "vulnerability_score": 8, "activity_frequency": 30, "historical_average": 3, "unknown_ip": True, "new_device": True, "abnormal_time": True}


async def test_analyze_and_read_results(client):
    response = await client.post("/api/ai/analyze", json=EVENT)
    assert response.status_code == 200
    result = response.json()["data"]
    assert result["anomaly"] is True
    assert result["risk_score"] >= 70
    for path in ("/api/ai/predictions", "/api/ai/risk-score", "/api/ai/alerts"):
        listing = await client.get(path)
        assert listing.status_code == 200
        assert listing.json()["data"]


async def test_validation_rejects_sensitive_fields(client):
    event = {**EVENT, "event_id": "invalid", "metadata": {"token": "secret"}}
    response = await client.post("/api/ai/analyze", json=event)
    assert response.status_code == 422


async def test_health_security_headers(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
