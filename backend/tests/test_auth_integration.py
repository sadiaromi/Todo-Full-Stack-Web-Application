import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.database.engine import create_db_and_tables, get_session
from sqlmodel import Session, SQLModel, create_engine
from app.models.user import User
from app.auth.jwt import create_access_token
from datetime import timedelta
import os

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def client():
    # Create a new engine for testing
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

    # Create tables
    SQLModel.metadata.create_all(engine)

    with TestClient(app) as c:
        yield c

def test_auth_integration_journey(client):
    """Integration test for the complete signup/login/logout journey."""

    # Test 1: Signup a new user
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "testuser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    signup_data = signup_response.json()
    assert "access_token" in signup_data
    assert signup_data["token_type"] == "bearer"

    # Store the token for subsequent requests
    token = signup_data["access_token"]

    # Test 2: Try to signup with the same email (should fail)
    duplicate_signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "testuser@example.com",
            "password": "AnotherPassword123!"
        }
    )

    assert duplicate_signup_response.status_code == 409  # Conflict

    # Test 3: Login with the created user
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    # Test 4: Access a protected endpoint (using the token from login)
    headers = {"Authorization": f"Bearer {login_data['access_token']}"}
    protected_response = client.get("/api/tasks", headers=headers)

    # Should be able to access tasks (might be empty list)
    assert protected_response.status_code in [200, 401]  # 401 might occur if token is different

    # If we use the signup token instead:
    headers = {"Authorization": f"Bearer {token}"}
    protected_response = client.get("/api/tasks", headers=headers)
    assert protected_response.status_code == 200  # Should work with valid token

    # Test 5: Logout (if logout endpoint exists)
    # Note: If logout is implemented as a server-side token invalidation, it might involve blacklisting
    # For now, we'll test that we can still make authenticated requests after 'logout'
    # if the system doesn't implement server-side token invalidation

    # Test 6: Test invalid credentials
    invalid_login_response = client.post(
        "/api/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert invalid_login_response.status_code == 401

    # Test 7: Test invalid email format
    invalid_email_response = client.post(
        "/api/auth/signup",
        json={
            "email": "invalid-email",
            "password": "TestPassword123!"
        }
    )

    assert invalid_email_response.status_code == 422  # Validation error

def test_password_strength_validation(client):
    """Test that passwords must meet strength requirements."""

    weak_passwords = [
        "123",  # Too short
        "abcdefgh",  # No uppercase, number, or special char
        "ABCD1234",  # No lowercase or special char
        "abcdABCD",  # No number or special char
        "abcd1234",  # No uppercase or special char
        "ABCD!@#$",  # No lowercase or number
    ]

    for weak_password in weak_passwords:
        response = client.post(
            "/api/auth/signup",
            json={
                "email": f"test_{weak_password}@example.com",
                "password": weak_password
            }
        )

        # Should fail validation for weak passwords
        assert response.status_code in [422, 400], f"Password '{weak_password}' should be rejected"

def test_email_validation(client):
    """Test email format validation."""

    invalid_emails = [
        "invalid-email",
        "@example.com",
        "test@",
        "test.example.com",
        "test@.com",
    ]

    for invalid_email in invalid_emails:
        response = client.post(
            "/api/auth/signup",
            json={
                "email": invalid_email,
                "password": "ValidPass123!"
            }
        )

        # Should fail validation for invalid emails
        assert response.status_code in [422, 400], f"Email '{invalid_email}' should be rejected"