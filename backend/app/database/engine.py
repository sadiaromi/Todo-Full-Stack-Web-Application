from sqlmodel import create_engine
from .config import settings
import os

# Use SQLite for easier setup
db_path = "todo_app.db"
database_url = f"sqlite:///{db_path}"

# Create the database engine
engine = create_engine(
    database_url,
    echo=settings.debug_mode,  # Set to True to see SQL queries in development
    connect_args={"check_same_thread": False}  # Required for SQLite
)