from sqlmodel import SQLModel, Field, Relationship, Column, String
from typing import Optional, List
import uuid
from datetime import datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False, max_length=255)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


# Need to import Task after User is defined to handle circular dependency
from .task import Task  # noqa: F401, E402

# Rebuild the model to handle the relationship
User.model_rebuild()