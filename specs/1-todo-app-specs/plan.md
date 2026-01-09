# Implementation Plan: Full-Stack Todo Web Application

**Feature**: Full-Stack Todo Web Application
**Branch**: 1-todo-app-specs
**Created**: 2026-01-06
**Status**: Draft

## Technical Context

### Architecture Overview
- **Frontend**: Next.js/React application with Better Auth integration
- **Backend**: FastAPI with SQLModel for database operations
- **Database**: PostgreSQL with proper relationships
- **Authentication**: JWT-based with Better Auth and refresh tokens
- **Security**: Token validation, ownership enforcement, rate limiting

### Technology Stack
- **Frontend Framework**: Next.js 14+
- **Backend Framework**: FastAPI 0.104+
- **Database ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: Better Auth
- **Database**: PostgreSQL
- **API Format**: RESTful JSON APIs

### Known Requirements from Spec
- User authentication (signup, login, logout)
- JWT token management with refresh tokens
- Task CRUD operations with ownership enforcement
- Rate limiting for authentication endpoints
- Password strength validation (8+ chars, upper, lower, number, special char)
- Task title limit (100 chars), description limit (1000 chars)
- Secure API endpoints with proper authorization

## Constitution Check

### Compliance Verification
- [x] All database queries filter by authenticated user ID
- [x] No direct database access from frontend
- [x] JWT tokens validated on all protected endpoints
- [x] User identity extracted from JWT, not URL parameters
- [x] Ownership enforcement on all task operations
- [x] Stateless authentication implementation
- [x] Proper error handling (401, 403, 404, 500 responses)

### Gate Evaluations
- **Authentication Security**: PASS - Using Better Auth with JWT validation
- **Data Security**: PASS - Ownership enforcement with user_id filtering
- **API Security**: PASS - All endpoints follow RESTful conventions with proper auth
- **Frontend Security**: PASS - No direct DB access, all via API

## Phase 0: Research & Preparation

### Research Tasks

#### 0.1 Better Auth Integration Research
- **Decision**: Use Better Auth with JWT for frontend authentication
- **Rationale**: Provides secure authentication with built-in best practices
- **Implementation**: Install better-auth package and configure with Next.js

#### 0.2 FastAPI JWT Middleware Research
- **Decision**: Implement custom JWT middleware for token validation
- **Rationale**: Provides consistent authentication across all protected endpoints
- **Implementation**: Create middleware that validates JWT and extracts user_id

#### 0.3 SQLModel Database Design Research
- **Decision**: Use SQLModel for database models with proper relationships
- **Rationale**: Combines SQLAlchemy and Pydantic for type safety
- **Implementation**: Define User and Task models with proper constraints

#### 0.4 Refresh Token Strategy Research
- **Decision**: Implement refresh token rotation for enhanced security
- **Rationale**: Provides seamless user experience while maintaining security
- **Implementation**: Issue short-lived access tokens with longer refresh tokens

## Phase 1: Data Model & API Design

### 1.1 Data Model Definition

#### User Model
```python
# File: backend/models/user.py
from sqlmodel import SQLModel, Field, Column, String
from typing import Optional
import uuid
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False, max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())
```

#### Task Model
```python
# File: backend/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime
from .user import User

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
    user: User = Relationship(back_populates="tasks")

# Update User model to include tasks relationship
User.model_rebuild()
```

### 1.2 API Contracts

#### Authentication Endpoints
```yaml
# File: specs/1-todo-app-specs/plan/contracts/auth.yaml
openapi: 3.0.0
info:
  title: Todo App Authentication API
  version: 1.0.0
paths:
  /api/auth/signup:
    post:
      summary: Create new user account
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                  pattern: "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*]).+$"
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
        '400':
          description: Validation error
        '409':
          description: Email already exists

  /api/auth/login:
    post:
      summary: Authenticate user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Authentication successful
          content:
            application.json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
        '401':
          description: Invalid credentials
```

#### Task Management Endpoints
```yaml
# File: specs/1-todo-app-specs/plan/contracts/tasks.yaml
openapi: 3.0.0
info:
  title: Todo App Task Management API
  version: 1.0.0
paths:
  /api/tasks:
    get:
      summary: Get user's tasks
      security:
        - bearerAuth: []
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [completed, incomplete, all]
      responses:
        '200':
          description: Tasks retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  tasks:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  total:
                    type: integer
    post:
      summary: Create new task
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Validation error
        '401':
          description: Unauthorized

  /api/tasks/{task_id}:
    get:
      summary: Get specific task
      security:
        - bearerAuth: []
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task retrieved successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '401':
          description: Unauthorized
        '403':
          description: Forbidden (not owner)
        '404':
          description: Task not found
    put:
      summary: Update task
      security:
        - bearerAuth: []
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Validation error
        '401':
          description: Unauthorized
        '403':
          description: Forbidden (not owner)
        '404':
          description: Task not found
    delete:
      summary: Delete task
      security:
        - bearerAuth: []
      parameters:
        - name: task_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task deleted successfully
        '401':
          description: Unauthorized
        '403':
          description: Forbidden (not owner)
        '404':
          description: Task not found

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
          maxLength: 100
        description:
          type: string
          maxLength: 1000
          nullable: true
        completed:
          type: boolean
        user_id:
          type: string
          format: uuid
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
    TaskCreate:
      type: object
      required: [title]
      properties:
        title:
          type: string
          maxLength: 100
        description:
          type: string
          maxLength: 1000
        completed:
          type: boolean
          default: false
    TaskUpdate:
      type: object
      properties:
        title:
          type: string
          maxLength: 100
        description:
          type: string
          maxLength: 1000
        completed:
          type: boolean
```

## Phase 2: Implementation Plan

### 1. Preparation

#### 1.1 Project Setup
- **Files**: `package.json`, `requirements.txt`, `.env.example`, `pyproject.toml`
- **Dependencies**: Install Next.js, FastAPI, SQLModel, Better Auth
- **Environment**: Set up environment variables for database, JWT secrets
- **@specs/1-todo-app-specs/spec.md**: Reference architecture requirements

#### 1.2 Directory Structure
```
project-root/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── api/
│   │   ├── auth/
│   │   └── database/
│   └── requirements.txt
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── lib/
│   └── package.json
├── specs/1-todo-app-specs/
└── .env.example
```

#### 1.3 Database Setup
- **Files**: `backend/app/database/engine.py`, `backend/app/database/init_db.py`
- **Setup**: PostgreSQL connection, SQLModel engine
- **@specs/1-todo-app-specs/database/schema.md**: Follow schema requirements

### 2. Backend Implementation

#### 2.1 FastAPI Application Setup
- **File**: `backend/app/main.py`
- **Implementation**: Initialize FastAPI app with CORS, middleware
- **@specs/1-todo-app-specs/api/rest-endpoints.md**: Follow API structure

#### 2.2 Database Models
- **Files**: `backend/app/models/user.py`, `backend/app/models/task.py`
- **Implementation**: Create SQLModel models with proper relationships
- **@specs/1-todo-app-specs/database/schema.md**: Follow schema design

#### 2.3 Database Session Management
- **File**: `backend/app/database/session.py`
- **Implementation**: Create database session dependency
- **@specs/1-todo-app-specs/database/schema.md**: Follow connection patterns

#### 2.4 Authentication Endpoints
- **File**: `backend/app/api/auth.py`
- **Implementation**: Create signup, login, logout endpoints
- **@specs/1-todo-app-specs/features/authentication.md**: Follow auth requirements
- **@specs/1-todo-app-specs/api/rest-endpoints.md**: Follow endpoint structure

#### 2.5 Task CRUD Endpoints
- **File**: `backend/app/api/tasks.py`
- **Implementation**: Create protected task endpoints with ownership validation
- **@specs/1-todo-app-specs/features/task-crud.md**: Follow CRUD requirements
- **@specs/1-todo-app-specs/api/rest-endpoints.md**: Follow endpoint structure

#### 2.6 JWT Middleware
- **File**: `backend/app/auth/jwt.py`
- **Implementation**: Create JWT validation middleware
- **@specs/1-todo-app-specs/features/authentication.md**: Follow JWT requirements
- **@specs/1-todo-app-specs/api/rest-endpoints.md**: Follow auth requirements

#### 2.7 Rate Limiting Implementation
- **File**: `backend/app/auth/rate_limit.py`
- **Implementation**: Implement rate limiting for auth endpoints
- **@specs/1-todo-app-specs/features/authentication.md**: Follow rate limiting (5 per 15 min)

### 3. Authentication Integration

#### 3.1 Better Auth Configuration
- **File**: `frontend/lib/auth.js`, `frontend/pages/api/auth/[...auth].js`
- **Implementation**: Configure Better Auth client and server
- **@specs/1-todo-app-specs/features/authentication.md**: Follow auth requirements

#### 3.2 JWT Token Management
- **File**: `frontend/lib/auth.js`, `frontend/lib/api.js`
- **Implementation**: Handle JWT token storage and refresh
- **@specs/1-todo-app-specs/features/authentication.md**: Follow token requirements

#### 3.3 Protected Route Component
- **File**: `frontend/components/ProtectedRoute.js`
- **Implementation**: Create component to protect authenticated routes
- **@specs/1-todo-app-specs/ui/pages.md**: Follow protected route behavior

### 4. Frontend Implementation

#### 4.1 Frontend Application Setup
- **File**: `frontend/pages/_app.js`, `frontend/package.json`
- **Implementation**: Initialize Next.js app with Better Auth provider
- **@specs/1-todo-app-specs/ui/pages.md**: Follow page structure

#### 4.2 Authentication Pages
- **Files**: `frontend/pages/login.js`, `frontend/pages/signup.js`
- **Implementation**: Create login and signup pages
- **@specs/1-todo-app-specs/ui/pages.md**: Follow login/signup page specs

#### 4.3 Dashboard Page
- **File**: `frontend/pages/index.js`
- **Implementation**: Create dashboard with task management
- **@specs/1-todo-app-specs/ui/pages.md**: Follow dashboard page specs

#### 4.4 Task Management Components
- **Files**: `frontend/components/TaskCard.js`, `frontend/components/TaskForm.js`
- **Implementation**: Create reusable task components
- **@specs/1-todo-app-specs/ui/components.md**: Follow component specs

#### 4.5 API Client
- **File**: `frontend/lib/api.js`
- **Implementation**: Create API client with JWT token handling
- **@specs/1-todo-app-specs/api/rest-endpoints.md**: Follow API structure

#### 4.6 Header Component
- **File**: `frontend/components/Header.js`
- **Implementation**: Create header with user controls
- **@specs/1-todo-app-specs/ui/components.md**: Follow header component specs

### 5. Security Validation

#### 5.1 Token Validation Testing
- **Implementation**: Test JWT validation in all protected endpoints
- **@specs/1-todo-app-specs/features/authentication.md**: Validate JWT requirements

#### 5.2 Ownership Enforcement Testing
- **Implementation**: Test that users can only access their own tasks
- **@specs/1-todo-app-specs/features/task-crud.md**: Validate ownership requirements

#### 5.3 Rate Limiting Testing
- **Implementation**: Test rate limiting on authentication endpoints
- **@specs/1-todo-app-specs/features/authentication.md**: Validate rate limits

#### 5.4 Input Validation Testing
- **Implementation**: Test all input validation requirements
- **@specs/1-todo-app-specs/ui/components.md**: Validate form requirements

### 6. Testing

#### 6.1 Unit Tests
- **Files**: `backend/tests/test_auth.py`, `backend/tests/test_tasks.py`
- **Implementation**: Create unit tests for backend functionality
- **@specs/1-todo-app-specs/spec.md**: Test functional requirements

#### 6.2 Integration Tests
- **Files**: `backend/tests/test_api.py`
- **Implementation**: Create integration tests for API endpoints
- **@specs/1-todo-app-specs/api/rest-endpoints.md**: Test API requirements

#### 6.3 Frontend Tests
- **Files**: `frontend/tests/*.test.js`
- **Implementation**: Create tests for frontend components
- **@specs/1-todo-app-specs/ui/components.md**: Test component functionality

### 7. Deployment Readiness

#### 7.1 Environment Configuration
- **Files**: `.env.production`, `Dockerfile`, `docker-compose.yml`
- **Implementation**: Prepare environment variables and deployment configs
- **@specs/1-todo-app-specs/architecture.md**: Follow architecture requirements

#### 7.2 Health Checks
- **File**: `backend/app/api/health.py`
- **Implementation**: Add health check endpoints for deployment
- **@specs/1-todo-app-specs/spec.md**: Follow reliability requirements

#### 7.3 Documentation
- **Files**: `README.md`, `docs/deployment.md`
- **Implementation**: Create deployment and usage documentation
- **@specs/1-todo-app-specs/spec.md**: Document feature capabilities

## Dependencies & Order of Implementation

### Critical Path Dependencies
1. **Database Models** → **Database Setup** → **API Endpoints**
2. **JWT Middleware** → **Authentication Endpoints** → **Task Endpoints**
3. **Better Auth Setup** → **Frontend Components** → **Protected Routes**
4. **API Client** → **Frontend Pages** → **Dashboard**

### Implementation Sequence
1. **Phase 1**: Database models and setup
2. **Phase 2**: Backend API with authentication
3. **Phase 3**: Frontend authentication integration
4. **Phase 4**: Frontend task management UI
5. **Phase 5**: Security validation and testing
6. **Phase 6**: Deployment preparation

## Success Criteria Verification

### Measurable Outcomes from Spec
- **SC-001**: Users can create accounts and log in within 2 minutes - Verified through UI testing
- **SC-002**: Users can CRUD tasks with <2 seconds response time - Verified through performance testing
- **SC-003**: 95% success rate on task creation - Verified through integration tests
- **SC-004**: Zero unauthorized access incidents - Verified through security testing
- **SC-005**: JWT tokens expire after 24 hours - Verified through token validation
- **SC-006**: Support for 100+ concurrent users - Verified through load testing

## Checklist for Implementation Completion

- [ ] All database models implemented per spec
- [ ] All API endpoints created per contract
- [ ] Authentication fully implemented with JWT
- [ ] Task CRUD operations with ownership enforcement
- [ ] Frontend components created per spec
- [ ] All security requirements met
- [ ] All tests passing
- [ ] Performance targets met
- [ ] Deployment configuration ready