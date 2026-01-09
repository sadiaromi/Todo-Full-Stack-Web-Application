"""
Contract tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.database.session import engine
from app.models.user import User


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


def test_signup_contract(client):
    """Test the signup endpoint contract"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    # Should return 200 or 409 (if email exists)
    assert response.status_code in [200, 409]

    # If successful, should return user and token
    if response.status_code == 200:
        data = response.json()
        assert "user" in data
        assert "id" in data["user"]
        assert "email" in data["user"]
        assert "token" in data
        assert isinstance(data["user"]["id"], str)
        assert data["user"]["email"] == "test@example.com"
        assert isinstance(data["token"], str)


def test_login_contract(client):
    """Test the login endpoint contract"""
    # First, try to login with a test user
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )

    # Should return 200 or 401
    assert response.status_code in [200, 401]

    # If successful, should return user and token
    if response.status_code == 200:
        data = response.json()
        assert "user" in data
        assert "id" in data["user"]
        assert "email" in data["user"]
        assert "token" in data


def test_logout_contract(client):
    """Test the logout endpoint contract"""
    # This test requires a valid token
    # For now, just check that the endpoint exists and returns expected status
    response = client.post("/api/auth/logout")

    # Should return 200 for successful logout
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Successfully logged out"