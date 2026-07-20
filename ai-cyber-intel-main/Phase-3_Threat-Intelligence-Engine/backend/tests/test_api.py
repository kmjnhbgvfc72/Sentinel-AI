import pytest

pytestmark = pytest.mark.anyio


async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"


@pytest.mark.parametrize("path", ["/api/threats", "/api/vulnerabilities", "/api/indicators", "/api/logs"])
async def test_collections(path, client):
    response = await client.get(path)
    assert response.status_code == 200
    assert response.json()["meta"]["total"] > 0


async def test_filters_and_statistics(client):
    response = await client.get("/api/threats", params={"severity": "critical"})
    assert all(item["severity"] == "critical" for item in response.json()["data"])
    statistics = (await client.get("/api/threat-statistics")).json()["data"]
    assert statistics["total_threats"] == sum(statistics["by_severity"].values())


async def test_validation(client):
    response = await client.get("/api/indicators", params={"page_size": 101})
    assert response.status_code == 422
