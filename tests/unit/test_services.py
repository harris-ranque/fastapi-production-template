
def test_create_item(client, sample_item):
    response = client.post("/api/items", json=sample_item)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_item["name"]
    assert data["description"] == sample_item["description"]