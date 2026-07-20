def test_invalid_token_rejected(client):
    assert (
        client.post(
            "/api/incidents",
            headers={"Authorization": "Bearer invalid"},
            json={"title": "Alert"},
        ).status_code
        == 401
    )
