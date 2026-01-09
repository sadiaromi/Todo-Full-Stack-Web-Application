from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
import uuid
from pydantic import BaseModel

from ..database.session import get_session
from ..auth.jwt import get_current_user
from ..services.task_service import TaskService
from ..models.task import Task

class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


router = APIRouter()


@router.get("/tasks")
async def get_tasks(
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user, optionally filtered by status."""
    task_service = TaskService(session)
    user_id = uuid.UUID(current_user["user_id"])

    tasks = task_service.get_user_tasks(user_id, status)

    # Format the response
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        })

    return {
        "tasks": tasks_data,
        "total": len(tasks_data)
    }


@router.post("/tasks")
async def create_task(
    task_data: CreateTaskRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user."""
    title = task_data.title
    description = task_data.description
    completed = task_data.completed

    # Validate task title length
    if len(title) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be 100 characters or less"
        )

    # Validate task description length
    if description and len(description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description must be 1000 characters or less"
        )

    task_service = TaskService(session)
    user_id = uuid.UUID(current_user["user_id"])

    task = task_service.create_task(
        user_id=user_id,
        title=title,
        description=description,
        completed=completed
    )

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "user_id": str(task.user_id),
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


@router.get("/tasks/{task_id}")
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for the current user."""
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task_service = TaskService(session)
    user_id = uuid.UUID(current_user["user_id"])

    task = task_service.get_task_by_id(task_uuid, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "user_id": str(task.user_id),
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: str,
    task_data: UpdateTaskRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for the current user."""
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    title = task_data.title
    description = task_data.description
    completed = task_data.completed

    # Validate task title length if provided
    if title and len(title) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be 100 characters or less"
        )

    # Validate task description length if provided
    if description and len(description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description must be 1000 characters or less"
        )

    task_service = TaskService(session)
    user_id = uuid.UUID(current_user["user_id"])

    task = task_service.update_task(
        task_id=task_uuid,
        user_id=user_id,
        title=title,
        description=description,
        completed=completed
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "user_id": str(task.user_id),
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task for the current user."""
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task_service = TaskService(session)
    user_id = uuid.UUID(current_user["user_id"])

    deleted = task_service.delete_task(task_uuid, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )

    return {"message": "Task deleted successfully"}