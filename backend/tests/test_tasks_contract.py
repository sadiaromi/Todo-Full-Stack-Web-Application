"""
Contract tests for task endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.database.session import engine


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_get_tasks_contract(client):
    """Test the get tasks endpoint contract"""
    # This test requires authentication
    # We'll test the expected response structure
    response = client.get("/api/tasks")

    # Should return 401 if no token provided
    assert response.status_code == 401

    # If we had a valid token, we'd expect:
    # - 200 status
    # - tasks array
    # - total count
    # data = response.json()
    # assert "tasks" in data
    # assert "total" in data


def test_create_task_contract(client):
    """Test the create task endpoint contract"""
    # This test requires authentication
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test task",
            "description": "Test description",
            "completed": False
        }
    )

    # Should return 401 if no token provided
    assert response.status_code == 401

    # With valid token, we'd expect:
    # - 200 or 201 status
    # - task object with all expected fields
    # data = response.json()
    # assert "id" in data
    # assert "title" in data
    # assert "completed" in data


def test_get_task_contract(client):
    """Test the get specific task endpoint contract"""
    # This test requires authentication
    response = client.get("/api/tasks/123e4567-e89b-12d3-a456-426614174000")

    # Should return 401 if no token provided
    assert response.status_code == 401

    # With valid token, we'd expect:
    # - 200 for success, 404 for not found, 403 for unauthorized access
    # - task object with all expected fields


def test_update_task_contract(client):
    """Test the update task endpoint contract"""
    # This test requires authentication
    response = client.put(
        "/api/tasks/123e4567-e89b-12d3-a456-426614174000",
        json={
            "title": "Updated task",
            "completed": True
        }
    )

    # Should return 401 if no token provided
    assert response.status_code == 401


def test_delete_task_contract(client):
    """Test the delete task endpoint contract"""
    # This test requires authentication
    response = client.delete("/api/tasks/123e4567-e89b-12d3-a456-426614174000")

    # Should return 401 if no token provided
    assert response.status_code == 401