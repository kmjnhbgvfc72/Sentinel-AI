def test_incident_lifecycle(client):
    created = client.post(
        "/api/incidents",
        json={"title": "Suspicious admin activity", "severity": "high"},
    )
    assert created.status_code == 201
    incident = created.json()
    assert client.get("/api/incidents").status_code == 200
    assert (
        client.patch(
            f"/api/incidents/{incident['id']}", json={"status": "contained"}
        ).json()["status"]
        == "contained"
    )
