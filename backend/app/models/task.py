from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime


class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=100)  # From spec clarification
    description: Optional[str] = Field(default=None, max_length=1000)  # From spec clarification
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

    # Relationship
    user: "User" = Relationship(back_populates="tasks")


# Import User after Task is defined to handle circular dependency
from .user import User  # noqa: F401, E402

# Rebuild the model to handle the relationship
Task.model_rebuild()