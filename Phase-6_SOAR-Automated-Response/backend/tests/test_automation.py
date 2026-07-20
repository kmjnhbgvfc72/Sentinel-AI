def test_safe_response(client):
    result = client.post(
        "/api/responses/recommend", params={"action": "Review account activity"}
    ).json()
    assert result["safe"] is True
