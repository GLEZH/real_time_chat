# tests/test_auth.py
from fastapi.testclient import TestClient


def test_register(client: TestClient):
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_register_existing_user(client: TestClient):
    # Попытка регистрации пользователя с тем же именем
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already exists"


def test_login(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"
