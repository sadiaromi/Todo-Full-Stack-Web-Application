from sqlmodel import Session, select
from typing import List, Optional
import uuid

from ..models.task import Task, TaskBase
from ..models.user import User


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, user_id: uuid.UUID, title: str, description: Optional[str] = None, completed: bool = False) -> Task:
        """Create a new task for a user."""
        task = Task(
            title=title,
            description=description,
            completed=completed,
            user_id=user_id
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_user_tasks(self, user_id: uuid.UUID, status: Optional[str] = None) -> List[Task]:
        """Get all tasks for a user, optionally filtered by status."""
        statement = select(Task).where(Task.user_id == user_id)

        if status:
            if status == "completed":
                statement = statement.where(Task.completed == True)
            elif status == "incomplete":
                statement = statement.where(Task.completed == False)

        statement = statement.order_by(Task.created_at.desc())
        return self.session.exec(statement).all()

    def get_task_by_id(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """Get a specific task by ID for a user (ensures ownership)."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return self.session.exec(statement).first()

    def update_task(self, task_id: uuid.UUID, user_id: uuid.UUID, title: Optional[str] = None,
                    description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Task]:
        """Update a task for a user (ensures ownership)."""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Delete a task for a user (ensures ownership)."""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_task_completion(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """Toggle the completion status of a task."""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task