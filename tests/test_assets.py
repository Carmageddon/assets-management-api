def test_add_asset(client):
    response = client.post("/api/assets/", json={
        "id": "1",
        "name": "Test Asset",
        "type": "ec2-instance",
        "tags": [{"key": "env", "value": "test"}],
        "cloud_account": {"id": "acc1", "name": "Test Account"},
        "owner_id": "owner1",
        "region": "us-west-1",
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Asset created successfully"

