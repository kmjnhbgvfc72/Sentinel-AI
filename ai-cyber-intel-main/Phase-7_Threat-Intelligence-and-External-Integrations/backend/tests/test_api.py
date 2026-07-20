def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["version"] == "7.0.0"


def test_ioc_lifecycle_and_reputation(client):
    payload = {"type": "ip", "value": "203.0.113.10", "threat_type": "simulated-probe", "confidence": 80, "severity": "high", "source": "unit-test", "tags": ["defensive-test"]}
    created = client.post("/api/ioc", json=payload)
    assert created.status_code == 201
    ioc_id = created.json()["id"]
    assert client.get("/api/ioc?type=ip").json()[0]["value"] == "203.0.113.10"
    reputation = client.get("/api/reputation/ip/203.0.113.10")
    assert reputation.status_code == 200
    assert reputation.json()["score"] >= 50
    assert client.delete(f"/api/ioc/{ioc_id}").status_code == 204


def test_invalid_ioc_has_structured_error(client):
    response = client.post("/api/ioc", json={"type": "ip", "value": "not-an-ip"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_ioc"


def test_summary(client):
    response = client.get("/api/intelligence/summary")
    assert response.status_code == 200
    assert response.json()["integration_phases"] == [3, 4, 5, 6]
