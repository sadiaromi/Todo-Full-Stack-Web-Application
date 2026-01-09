from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, tasks, health
from .database.config import settings
from .database.engine import engine
from sqlmodel import SQLModel

# Import models to register them with SQLModel for table creation
from .models import user, task

# Import security middleware
from .security.middleware import add_security_middleware


app = FastAPI(
    title="Todo App API",
    description="Full-Stack Todo Web Application API",
    version="1.0.0"
)

# Add security middleware
add_security_middleware(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix=settings.api_prefix, tags=["authentication"])
app.include_router(tasks.router, prefix=settings.api_prefix, tags=["tasks"])
app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])


@app.on_event("startup")
def on_startup():
    # Create database tables
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}