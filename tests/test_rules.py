def test_add_rule(client):
    response = client.post("/api/rules/", json={
        "owner_id": "owner1",
        "group_name": "production",
        "conditions": {
            "type": "ec2-instance",
            "tags": {"env": "prod"},
            "name_contains": "prod"
        },
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Rule created successfully"

def test_group_assets(client):
    client.post("/api/assets/", json={
        "id": "1",
        "name": "prod-instance",
        "type": "ec2-instance",
        "tags": [{"key": "env", "value": "prod"}],
        "cloud_account": {"id": "acc1", "name": "Test Account"},
        "owner_id": "owner1",
        "region": "us-west-1",
    })
    
    client.post("/api/rules/", json={
        "owner_id": "owner1",
        "group_name": "production",
        "conditions": {
            "type": "ec2-instance",
            "tags": {"env": "prod"},
            "name_contains": "prod"
        },
    })

    response = client.post("/api/owners/owner1/apply-rules", json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Assets grouped successfully"

    asset_response = client.get("/api/assets/")
    assets = asset_response.get_json()
    assert assets[0]["group_name"] == "production"
