import pytest

pytestmark = pytest.mark.anyio


async def test_health_endpoints(client):
    for path in ("/health", "/api/health"):
        response = await client.get(path)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


async def test_dashboard_summary(client):
    response = await client.get("/api/dashboard/summary")
    assert response.status_code == 200
    assert response.json()["data"]["protected_assets"] > 0
    assert 0 <= response.json()["data"]["risk"]["score"] <= 100


async def test_threat_listing_and_filtering(client):
    response = await client.get("/api/threats", params={"severity": "critical", "page_size": 10})
    assert response.status_code == 200
    assert response.json()["meta"]["total"] == 1
    assert all(item["severity"] == "critical" for item in response.json()["data"])


async def test_threat_details(client):
    response = await client.get("/api/threats/1")
    assert response.status_code == 200
    assert response.json()["data"]["external_id"] == "THR-2026-1042"


async def test_alert_listing(client):
    response = await client.get("/api/alerts", params={"status": "new"})
    assert response.status_code == 200
    assert response.json()["meta"]["total"] == 1


async def test_valid_alert_status_transition(client):
    response = await client.patch("/api/alerts/1/status", json={"status": "acknowledged", "changed_by": "test-analyst"})
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "acknowledged"


async def test_invalid_alert_status_transition(client):
    response = await client.patch("/api/alerts/4/status", json={"status": "acknowledged"})
    assert response.status_code == 409
    assert "not allowed" in response.json()["detail"]


async def test_pagination_validation(client):
    response = await client.get("/api/threats", params={"page_size": 101})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


async def test_missing_records(client):
    assert (await client.get("/api/threats/999")).status_code == 404
    assert (await client.get("/api/alerts/999")).status_code == 404
    assert (await client.get("/api/assets/999")).status_code == 404


async def test_security_headers(client):
    response = await client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
