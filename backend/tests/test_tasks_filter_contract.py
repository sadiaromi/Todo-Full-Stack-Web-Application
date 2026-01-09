import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.engine import create_db_and_tables
from app.auth.jwt import create_access_token
from datetime import timedelta
from sqlmodel import Session, SQLModel, create_engine
import os

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///./test_contract.db"

@pytest.fixture(scope="function")
def client():
    # Create a new engine for testing
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

    # Create tables
    SQLModel.metadata.create_all(engine)

    with TestClient(app) as c:
        yield c

def test_get_tasks_endpoint_contract(client):
    """Contract test for GET /api/tasks endpoint."""

    # Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "contractuser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    token = signup_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test GET /api/tasks without status parameter
    response = client.get("/api/tasks", headers=headers)

    assert response.status_code == 200
    data = response.json()

    # Contract: Response should contain 'tasks' key with a list
    assert "tasks" in data
    assert isinstance(data["tasks"], list)

    # Contract: Each task should have expected properties
    if data["tasks"]:
        task = data["tasks"][0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task
        assert "user_id" in task

def test_get_tasks_with_status_parameter_contract(client):
    """Contract test for GET /api/tasks endpoint with status parameter."""

    # Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "contractuser2@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    token = signup_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test GET /api/tasks with status parameter
    valid_statuses = ["all", "completed", "incomplete"]

    for status in valid_statuses:
        response = client.get(f"/api/tasks?status={status}", headers=headers)

        assert response.status_code == 200
        data = response.json()

        # Contract: Response should contain 'tasks' key with a list
        assert "tasks" in data
        assert isinstance(data["tasks"], list)

def test_invalid_status_parameter_contract(client):
    """Contract test for GET /api/tasks endpoint with invalid status parameter."""

    # Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "contractuser3@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    token = signup_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test GET /api/tasks with invalid status parameter
    response = client.get("/api/tasks?status=invalid", headers=headers)

    # Should return 422 Unprocessable Entity for invalid status
    assert response.status_code in [422, 400]

def test_get_tasks_authentication_contract(client):
    """Contract test for GET /api/tasks endpoint authentication."""

    # Test GET /api/tasks without authentication
    response = client.get("/api/tasks")

    # Should return 401 Unauthorized
    assert response.status_code == 401

def test_update_task_completion_contract(client):
    """Contract test for PUT /api/tasks/{id} endpoint for toggling completion."""

    # Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "contractuser4@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    token = signup_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task first
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task for Contract",
            "description": "Test description",
            "completed": False
        },
        headers=headers
    )

    assert create_response.status_code == 200
    task_data = create_response.json()
    task_id = task_data["id"]

    # Test PUT /api/tasks/{id} to update completion status
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "completed": True
        },
        headers=headers
    )

    assert update_response.status_code == 200
    updated_task = update_response.json()

    # Contract: Updated task should have expected properties
    assert "id" in updated_task
    assert "title" in updated_task
    assert "description" in updated_task
    assert "completed" in updated_task
    assert updated_task["completed"] is True  # Should be updated to True
    assert "created_at" in updated_task
    assert "updated_at" in updated_task
    assert "user_id" in updated_task

def test_task_ownership_contract(client):
    """Contract test for task ownership enforcement."""

    # Create first user
    signup_response1 = client.post(
        "/api/auth/signup",
        json={
            "email": "owner1@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response1.status_code == 200
    token1 = signup_response1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Create second user
    signup_response2 = client.post(
        "/api/auth/signup",
        json={
            "email": "owner2@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response2.status_code == 200
    token2 = signup_response2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # First user creates a task
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Owner's Task",
            "description": "This belongs to owner1",
            "completed": False
        },
        headers=headers1
    )

    assert create_response.status_code == 200
    task_data = create_response.json()
    task_id = task_data["id"]

    # Second user tries to update the task (should fail)
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "completed": True
        },
        headers=headers2
    )

    # Should return 404 Not Found or 403 Forbidden
    assert update_response.status_code in [404, 403]

def test_task_filtering_by_status_contract(client):
    """Contract test for task filtering by status functionality."""

    # Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "filteruser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    token = signup_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create multiple tasks with different completion statuses
    task1_response = client.post(
        "/api/tasks",
        json={
            "title": "Completed Task",
            "description": "This is completed",
            "completed": True
        },
        headers=headers
    )

    task2_response = client.post(
        "/api/tasks",
        json={
            "title": "Incomplete Task",
            "description": "This is not completed",
            "completed": False
        },
        headers=headers
    )

    assert task1_response.status_code == 200
    assert task2_response.status_code == 200

    # Test filtering for completed tasks
    completed_response = client.get("/api/tasks?status=completed", headers=headers)
    assert completed_response.status_code == 200
    completed_tasks = completed_response.json()["tasks"]

    # Contract: Should only return completed tasks
    for task in completed_tasks:
        assert task["completed"] is True

    # Test filtering for incomplete tasks
    incomplete_response = client.get("/api/tasks?status=incomplete", headers=headers)
    assert incomplete_response.status_code == 200
    incomplete_tasks = incomplete_response.json()["tasks"]

    # Contract: Should only return incomplete tasks
    for task in incomplete_tasks:
        assert task["completed"] is False

    # Test filtering for all tasks
    all_response = client.get("/api/tasks?status=all", headers=headers)
    assert all_response.status_code == 200
    all_tasks = all_response.json()["tasks"]

    # Contract: Should return all tasks regardless of status
    assert len(all_tasks) >= 2  # At least the 2 tasks we created