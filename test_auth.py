from conftest import client
import uuid


def test_register_admin():

    email = f"admin{uuid.uuid4().hex[:6]}@test.com"

    response = client.post(
        "/auth/register",
        json={
            "username": "Admin",
            "email": email,
            "password": "admin123",
            "role": "Admin"
        }
    )

    assert response.status_code == 200


def test_login():

    email = f"login{uuid.uuid4().hex[:6]}@test.com"

    # Register user first
    register_response = client.post(
        "/auth/register",
        json={
            "username": "Login Admin",
            "email": email,
            "password": "admin123",
            "role": "Admin"
        }
    )

    assert register_response.status_code == 200


    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"