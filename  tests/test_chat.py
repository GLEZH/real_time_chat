from fastapi.testclient import TestClient


def get_auth_token(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass"}
    )
    return response.json()["access_token"]


def test_get_rooms(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/chat/rooms", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_room(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/chat/rooms",
        json={"name": "Test Room"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Room"
    assert "id" in data


def test_create_existing_room(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/chat/rooms",
        json={"name": "Test Room"},
        headers=headers
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Room already exists"
