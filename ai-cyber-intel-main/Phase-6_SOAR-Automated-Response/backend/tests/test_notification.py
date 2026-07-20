def test_notification(client):
    response = client.post(
        "/api/notifications",
        json={
            "channel": "webhook",
            "recipient": "https://example.invalid/hook",
            "subject": "Alert",
        },
    )
    assert response.status_code == 201
