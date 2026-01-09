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
DATABASE_URL = "sqlite:///./test_filter_integration.db"

@pytest.fixture(scope="function")
def client():
    # Create a new engine for testing
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

    # Create tables
    SQLModel.metadata.create_all(engine)

    with TestClient(app) as c:
        yield c

def test_task_filtering_integration(client):
    """Integration test for the complete task filtering journey."""

    # Step 1: Create a user account
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "filteruser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    signup_data = signup_response.json()
    assert "access_token" in signup_data
    token = signup_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Create multiple tasks with different completion statuses
    # Create 2 completed tasks
    completed_task_1 = client.post(
        "/api/tasks",
        json={
            "title": "Completed Task 1",
            "description": "This is a completed task",
            "completed": True
        },
        headers=headers
    )

    completed_task_2 = client.post(
        "/api/tasks",
        json={
            "title": "Completed Task 2",
            "description": "This is another completed task",
            "completed": True
        },
        headers=headers
    )

    # Create 2 incomplete tasks
    incomplete_task_1 = client.post(
        "/api/tasks",
        json={
            "title": "Incomplete Task 1",
            "description": "This is an incomplete task",
            "completed": False
        },
        headers=headers
    )

    incomplete_task_2 = client.post(
        "/api/tasks",
        json={
            "title": "Incomplete Task 2",
            "description": "This is another incomplete task",
            "completed": False
        },
        headers=headers
    )

    # Verify all tasks were created successfully
    assert completed_task_1.status_code == 200
    assert completed_task_2.status_code == 200
    assert incomplete_task_1.status_code == 200
    assert incomplete_task_2.status_code == 200

    # Store task IDs for later verification
    completed_task_1_id = completed_task_1.json()["id"]
    completed_task_2_id = completed_task_2.json()["id"]
    incomplete_task_1_id = incomplete_task_1.json()["id"]
    incomplete_task_2_id = incomplete_task_2.json()["id"]

    # Step 3: Test filtering for all tasks (status=all)
    all_tasks_response = client.get("/api/tasks?status=all", headers=headers)
    assert all_tasks_response.status_code == 200
    all_tasks_data = all_tasks_response.json()
    assert "tasks" in all_tasks_data
    assert len(all_tasks_data["tasks"]) == 4  # All 4 tasks should be returned

    # Verify all tasks are present
    task_ids = [task["id"] for task in all_tasks_data["tasks"]]
    assert completed_task_1_id in task_ids
    assert completed_task_2_id in task_ids
    assert incomplete_task_1_id in task_ids
    assert incomplete_task_2_id in task_ids

    # Step 4: Test filtering for completed tasks only
    completed_tasks_response = client.get("/api/tasks?status=completed", headers=headers)
    assert completed_tasks_response.status_code == 200
    completed_tasks_data = completed_tasks_response.json()
    assert "tasks" in completed_tasks_data
    assert len(completed_tasks_data["tasks"]) == 2  # Only 2 completed tasks

    # Verify only completed tasks are returned
    completed_task_ids = [task["id"] for task in completed_tasks_data["tasks"]]
    assert completed_task_1_id in completed_task_ids
    assert completed_task_2_id in completed_task_ids
    assert incomplete_task_1_id not in completed_task_ids
    assert incomplete_task_2_id not in completed_task_ids

    # Verify all returned tasks are indeed completed
    for task in completed_tasks_data["tasks"]:
        assert task["completed"] is True

    # Step 5: Test filtering for incomplete tasks only
    incomplete_tasks_response = client.get("/api/tasks?status=incomplete", headers=headers)
    assert incomplete_tasks_response.status_code == 200
    incomplete_tasks_data = incomplete_tasks_response.json()
    assert "tasks" in incomplete_tasks_data
    assert len(incomplete_tasks_data["tasks"]) == 2  # Only 2 incomplete tasks

    # Verify only incomplete tasks are returned
    incomplete_task_ids = [task["id"] for task in incomplete_tasks_data["tasks"]]
    assert incomplete_task_1_id in incomplete_task_ids
    assert incomplete_task_2_id in incomplete_task_ids
    assert completed_task_1_id not in incomplete_task_ids
    assert completed_task_2_id not in incomplete_task_ids

    # Verify all returned tasks are indeed incomplete
    for task in incomplete_tasks_data["tasks"]:
        assert task["completed"] is False

    # Step 6: Test default behavior (no status parameter) - should return all tasks
    default_response = client.get("/api/tasks", headers=headers)
    assert default_response.status_code == 200
    default_data = default_response.json()
    assert "tasks" in default_data
    assert len(default_data["tasks"]) == 4  # All 4 tasks should be returned

    # Step 7: Update a task's completion status and verify filtering still works correctly
    # Update one of the incomplete tasks to be completed
    update_response = client.put(
        f"/api/tasks/{incomplete_task_1_id}",
        json={
            "completed": True
        },
        headers=headers
    )

    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["id"] == incomplete_task_1_id
    assert updated_task["completed"] is True

    # Step 8: Re-test filtering after the update
    # Completed tasks should now have 3 tasks
    updated_completed_response = client.get("/api/tasks?status=completed", headers=headers)
    assert updated_completed_response.status_code == 200
    updated_completed_data = updated_completed_response.json()
    assert len(updated_completed_data["tasks"]) == 3  # Now 3 completed tasks

    # Incomplete tasks should now have 1 task
    updated_incomplete_response = client.get("/api/tasks?status=incomplete", headers=headers)
    assert updated_incomplete_response.status_code == 200
    updated_incomplete_data = updated_incomplete_response.json()
    assert len(updated_incomplete_data["tasks"]) == 1  # Now only 1 incomplete task

    # All tasks should still have 4 tasks total
    updated_all_response = client.get("/api/tasks?status=all", headers=headers)
    assert updated_all_response.status_code == 200
    updated_all_data = updated_all_response.json()
    assert len(updated_all_data["tasks"]) == 4  # Still 4 tasks total

def test_task_filtering_with_multiple_users(client):
    """Test that task filtering works correctly with multiple users."""

    # Create first user
    signup_response1 = client.post(
        "/api/auth/signup",
        json={
            "email": "user1_filter@example.com",
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
            "email": "user2_filter@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response2.status_code == 200
    user2_token = signup_response2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    # User 1 creates 2 tasks (1 completed, 1 incomplete)
    user1_task1 = client.post(
        "/api/tasks",
        json={
            "title": "User 1 Completed Task",
            "description": "This belongs to user 1",
            "completed": True
        },
        headers=headers1
    )

    user1_task2 = client.post(
        "/api/tasks",
        json={
            "title": "User 1 Incomplete Task",
            "description": "This belongs to user 1",
            "completed": False
        },
        headers=headers1
    )

    assert user1_task1.status_code == 200
    assert user1_task2.status_code == 200

    # User 2 creates 2 tasks (1 completed, 1 incomplete)
    user2_task1 = client.post(
        "/api/tasks",
        json={
            "title": "User 2 Completed Task",
            "description": "This belongs to user 2",
            "completed": True
        },
        headers=headers2
    )

    user2_task2 = client.post(
        "/api/tasks",
        json={
            "title": "User 2 Incomplete Task",
            "description": "This belongs to user 2",
            "completed": False
        },
        headers=headers2
    )

    assert user2_task1.status_code == 200
    assert user2_task2.status_code == 200

    # User 1 should only see their own tasks when filtering
    user1_completed_response = client.get("/api/tasks?status=completed", headers=headers1)
    assert user1_completed_response.status_code == 200
    user1_completed_tasks = user1_completed_response.json()["tasks"]
    assert len(user1_completed_tasks) == 1  # Only user 1's completed task
    assert user1_completed_tasks[0]["title"] == "User 1 Completed Task"

    user1_incomplete_response = client.get("/api/tasks?status=incomplete", headers=headers1)
    assert user1_incomplete_response.status_code == 200
    user1_incomplete_tasks = user1_incomplete_response.json()["tasks"]
    assert len(user1_incomplete_tasks) == 1  # Only user 1's incomplete task
    assert user1_incomplete_tasks[0]["title"] == "User 1 Incomplete Task"

    # User 2 should only see their own tasks when filtering
    user2_completed_response = client.get("/api/tasks?status=completed", headers=headers2)
    assert user2_completed_response.status_code == 200
    user2_completed_tasks = user2_completed_response.json()["tasks"]
    assert len(user2_completed_tasks) == 1  # Only user 2's completed task
    assert user2_completed_tasks[0]["title"] == "User 2 Completed Task"

    user2_incomplete_response = client.get("/api/tasks?status=incomplete", headers=headers2)
    assert user2_incomplete_response.status_code == 200
    user2_incomplete_tasks = user2_incomplete_response.json()["tasks"]
    assert len(user2_incomplete_tasks) == 1  # Only user 2's incomplete task
    assert user2_incomplete_tasks[0]["title"] == "User 2 Incomplete Task"

def test_task_filtering_edge_cases(client):
    """Test edge cases for task filtering."""

    # Create a user
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "edgecaseuser@example.com",
            "password": "TestPassword123!"
        }
    )

    assert signup_response.status_code == 200
    token = signup_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test with no tasks - all filters should return empty arrays
    all_empty_response = client.get("/api/tasks?status=all", headers=headers)
    assert all_empty_response.status_code == 200
    assert all_empty_response.json()["tasks"] == []

    completed_empty_response = client.get("/api/tasks?status=completed", headers=headers)
    assert completed_empty_response.status_code == 200
    assert completed_empty_response.json()["tasks"] == []

    incomplete_empty_response = client.get("/api/tasks?status=incomplete", headers=headers)
    assert incomplete_empty_response.status_code == 200
    assert incomplete_empty_response.json()["tasks"] == []

    # Create one task
    task_response = client.post(
        "/api/tasks",
        json={
            "title": "Single Task",
            "description": "Just one task",
            "completed": False
        },
        headers=headers
    )

    assert task_response.status_code == 200

    # Test filtering again with one task
    all_single_response = client.get("/api/tasks?status=all", headers=headers)
    assert len(all_single_response.json()["tasks"]) == 1

    completed_single_response = client.get("/api/tasks?status=completed", headers=headers)
    assert len(completed_single_response.json()["tasks"]) == 0  # No completed tasks

    incomplete_single_response = client.get("/api/tasks?status=incomplete", headers=headers)
    assert len(incomplete_single_response.json()["tasks"]) == 1  # One incomplete task