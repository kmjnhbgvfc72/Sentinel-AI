def test_playbooks_and_workflow(client):
    assert client.get("/api/playbooks").status_code == 200
    incident = client.post("/api/incidents", json={"title": "Test alert"}).json()
    assert client.post(f"/api/playbooks/execute/{incident['id']}").status_code == 200
