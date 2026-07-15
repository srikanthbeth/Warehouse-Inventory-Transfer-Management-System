import sys
import os
import pytest

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


@pytest.fixture(scope="session")
def test_user():

    response = client.post(
        "/auth/register",
        json={
            "username": "Test Admin",
            "email": "admin@test.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    # User already exists is okay
    if response.status_code not in [200, 400]:
        print(response.json())

    return {
        "email": "admin@test.com",
        "password": "admin123"
    }


@pytest.fixture(scope="session")
def token(test_user):

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )

    print("LOGIN RESPONSE:", response.json())

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def headers(token):

    return {
        "Authorization": f"Bearer {token}"
    }