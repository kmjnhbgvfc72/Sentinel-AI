"""FastAPI contract tests."""


def test_health_and_openapi(client) -> None:
    assert client.get("/health").status_code == 200
    schema = client.get("/openapi.json").json()
    assert "/api/v1/hunting/search" in schema["paths"]


def test_ioc_creation_and_hunt(client) -> None:
    created = client.post("/api/v1/intelligence/iocs", json={"type": "domain", "value": "malicious.example", "confidence": 0.95, "source": "test"})
    assert created.status_code == 201
    hunted = client.post("/api/v1/hunting/search", json={"id": "event-1", "text": "Connected to malicious.example", "behaviors": []})
    assert hunted.status_code == 200
    assert hunted.json()["ioc_matches"][0]["confidence"] == 0.95


def test_learning_api(client) -> None:
    response = client.post("/api/v1/learning/retrain", json={"samples": [[0, 0], [0.1, 0.2], [8, 9]]})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
