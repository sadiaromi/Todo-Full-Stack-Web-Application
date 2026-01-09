import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.database.engine import create_db_and_tables, get_session
from sqlmodel import Session, SQLModel, create_engine
from app.models.user import User
from app.models.task import Task
from app.auth.jwt import create_access_token
from datetime import timedelta
import os

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///./test_tasks.db"

@pytest.fixture(scope="function")
def client():
    # Create a new engine for testing
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

    # Create tables
    SQLModel.metadata.create_all(engine)

    with TestClient(app) as c:
        yield c

def test_task_crud_integration(client):
    """Integration test for complete task CRUD operations."""

    # Step 1: Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "taskuser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    signup_data = signup_response.json()
    assert "access_token" in signup_data
    token = signup_data["access_token"]

    # Step 2: Create headers with the token
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Test creating a task
    create_task_response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task 1",
            "description": "This is a test task description",
            "completed": False
        },
        headers=headers
    )

    assert create_task_response.status_code == 200
    created_task = create_task_response.json()
    assert created_task["title"] == "Test Task 1"
    assert created_task["description"] == "This is a test task description"
    assert created_task["completed"] is False
    assert "id" in created_task
    task_id = created_task["id"]

    # Step 4: Test reading all tasks
    get_tasks_response = client.get("/api/tasks", headers=headers)
    assert get_tasks_response.status_code == 200
    tasks_data = get_tasks_response.json()
    assert "tasks" in tasks_data
    assert len(tasks_data["tasks"]) == 1
    assert tasks_data["tasks"][0]["id"] == task_id

    # Step 5: Test reading tasks with filtering (all)
    get_all_tasks_response = client.get("/api/tasks?status=all", headers=headers)
    assert get_all_tasks_response.status_code == 200
    all_tasks_data = get_all_tasks_response.json()
    assert len(all_tasks_data["tasks"]) == 1

    # Step 6: Test reading tasks with filtering (incomplete)
    get_incomplete_tasks_response = client.get("/api/tasks?status=incomplete", headers=headers)
    assert get_incomplete_tasks_response.status_code == 200
    incomplete_tasks_data = get_incomplete_tasks_response.json()
    assert len(incomplete_tasks_data["tasks"]) == 1

    # Step 7: Test reading tasks with filtering (completed)
    get_completed_tasks_response = client.get("/api/tasks?status=completed", headers=headers)
    assert get_completed_tasks_response.status_code == 200
    completed_tasks_data = get_completed_tasks_response.json()
    assert len(completed_tasks_data["tasks"]) == 0

    # Step 8: Test updating a task
    update_task_response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Updated Test Task 1",
            "description": "Updated description",
            "completed": True
        },
        headers=headers
    )

    assert update_task_response.status_code == 200
    updated_task = update_task_response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Test Task 1"
    assert updated_task["description"] == "Updated description"
    assert updated_task["completed"] is True

    # Step 9: Verify the update by getting the task again
    get_updated_task_response = client.get(f"/api/tasks", headers=headers)
    assert get_updated_task_response.status_code == 200
    updated_tasks = get_updated_task_response.json()["tasks"]
    assert len(updated_tasks) == 1
    assert updated_tasks[0]["title"] == "Updated Test Task 1"
    assert updated_tasks[0]["completed"] is True

    # Step 10: Test creating another task
    create_second_task_response = client.post(
        "/api/tasks",
        json={
            "title": "Second Test Task",
            "description": "This is the second test task",
            "completed": False
        },
        headers=headers
    )

    assert create_second_task_response.status_code == 200
    second_task = create_second_task_response.json()
    assert second_task["title"] == "Second Test Task"
    assert second_task["completed"] is False
    second_task_id = second_task["id"]

    # Step 11: Verify both tasks exist
    get_all_tasks_response = client.get("/api/tasks", headers=headers)
    assert get_all_tasks_response.status_code == 200
    all_tasks = get_all_tasks_response.json()["tasks"]
    assert len(all_tasks) == 2

    # Step 12: Test filtering for completed tasks (should be 1 now)
    get_completed_tasks_response = client.get("/api/tasks?status=completed", headers=headers)
    assert get_completed_tasks_response.status_code == 200
    completed_tasks_data = get_completed_tasks_response.json()
    assert len(completed_tasks_data["tasks"]) == 1

    # Step 13: Test filtering for incomplete tasks (should be 1 now)
    get_incomplete_tasks_response = client.get("/api/tasks?status=incomplete", headers=headers)
    assert get_incomplete_tasks_response.status_code == 200
    incomplete_tasks_data = get_incomplete_tasks_response.json()
    assert len(incomplete_tasks_data["tasks"]) == 1

    # Step 14: Test deleting a task
    delete_task_response = client.delete(f"/api/tasks/{second_task_id}", headers=headers)
    assert delete_task_response.status_code == 200

    # Step 15: Verify the deleted task is gone
    get_remaining_tasks_response = client.get("/api/tasks", headers=headers)
    assert get_remaining_tasks_response.status_code == 200
    remaining_tasks = get_remaining_tasks_response.json()["tasks"]
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0]["id"] == task_id

def test_task_validation(client):
    """Test task validation rules."""

    # Step 1: Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "validuser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    signup_data = signup_response.json()
    token = signup_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test 1: Title too long (max 100 chars)
    long_title = "A" * 101
    response = client.post(
        "/api/tasks",
        json={
            "title": long_title,
            "description": "Short description",
            "completed": False
        },
        headers=headers
    )

    # Should fail validation
    assert response.status_code in [422, 400]

    # Test 2: Description too long (max 1000 chars)
    long_description = "A" * 1001
    response = client.post(
        "/api/tasks",
        json={
            "title": "Valid title",
            "description": long_description,
            "completed": False
        },
        headers=headers
    )

    # Should fail validation
    assert response.status_code in [422, 400]

    # Test 3: Valid task creation
    response = client.post(
        "/api/tasks",
        json={
            "title": "Valid task title",
            "description": "Valid description within limits",
            "completed": False
        },
        headers=headers
    )

    assert response.status_code == 200

def test_task_ownership(client):
    """Test that users can only access their own tasks."""

    # Create first user
    signup_response1 = client.post(
        "/api/auth/signup",
        json={
            "email": "user1@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response1.status_code == 200
    user1_token = signup_response1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {user1_token}"}

    # Create second user
    signup_response2 = client.post(
        "/api/auth/signup",
        json={
            "email": "user2@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response2.status_code == 200
    user2_token = signup_response2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    # User 1 creates a task
    create_task_response = client.post(
        "/api/tasks",
        json={
            "title": "User 1's task",
            "description": "This belongs to user 1",
            "completed": False
        },
        headers=headers1
    )

    assert create_task_response.status_code == 200
    task_data = create_task_response.json()
    task_id = task_data["id"]

    # User 1 should see their task
    get_tasks_response1 = client.get("/api/tasks", headers=headers1)
    assert get_tasks_response1.status_code == 200
    user1_tasks = get_tasks_response1.json()["tasks"]
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] == task_id

    # User 2 should not see user 1's task
    get_tasks_response2 = client.get("/api/tasks", headers=headers2)
    assert get_tasks_response2.status_code == 200
    user2_tasks = get_tasks_response2.json()["tasks"]
    assert len(user2_tasks) == 0

    # User 2 tries to access user 1's specific task (should fail)
    specific_task_response = client.get(f"/api/tasks/{task_id}", headers=headers2)
    assert specific_task_response.status_code in [404, 403]  # Not found or forbidden