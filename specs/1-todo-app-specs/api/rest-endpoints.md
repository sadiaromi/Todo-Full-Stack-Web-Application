# API Specification: REST Endpoints for Todo Application

## Base URLs
- **Development**: `http://localhost:8000/api/`
- **Production**: `https://[domain]/api/`

## Auth Requirements
- **Public Endpoints**: No authentication required (signup, login)
- **Protected Endpoints**: JWT token required in `Authorization: Bearer <token>` header
- **Token Validation**: All protected endpoints MUST validate JWT tokens
- **User Context**: Valid tokens MUST provide user identity for request processing

## All CRUD Endpoints

### Authentication Endpoints (Public)

#### POST /api/auth/signup
- **Auth Required**: No
- **Purpose**: Create new user account
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Response Success (201)**:
  ```json
  {
    "user": {
      "id": "user-uuid",
      "email": "user@example.com"
    },
    "token": "jwt-token-string"
  }
  ```
- **Response Errors**: 400 (validation), 409 (duplicate email), 500 (server error)

#### POST /api/auth/login
- **Auth Required**: No
- **Purpose**: Authenticate user and return JWT token
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```
- **Response Success (200)**:
  ```json
  {
    "user": {
      "id": "user-uuid",
      "email": "user@example.com"
    },
    "token": "jwt-token-string"
  }
  ```
- **Response Errors**: 400 (validation), 401 (invalid credentials), 500 (server error)

#### POST /api/auth/logout
- **Auth Required**: Yes (valid JWT)
- **Purpose**: Logout user (client-side token removal)
- **Request Body**: None
- **Response Success (200)**:
  ```json
  {
    "message": "Successfully logged out"
  }
  ```
- **Response Errors**: 401 (invalid/missing token), 500 (server error)

### Task Management Endpoints (Protected)

#### GET /api/tasks
- **Auth Required**: Yes
- **Purpose**: Get all tasks for authenticated user
- **Query Parameters**:
  - `status` (optional): "completed", "incomplete", or "all" (default: "all")
  - `limit` (optional): Number of tasks to return (default: 50)
  - `offset` (optional): Number of tasks to skip (default: 0)
- **Response Success (200)**:
  ```json
  {
    "tasks": [
      {
        "id": "task-uuid",
        "title": "Task title",
        "description": "Task description",
        "completed": false,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
      }
    ],
    "total": 15,
    "limit": 50,
    "offset": 0
  }
  ```
- **Response Errors**: 401 (invalid/missing token), 500 (server error)

#### POST /api/tasks
- **Auth Required**: Yes
- **Purpose**: Create a new task for authenticated user
- **Request Body**:
  ```json
  {
    "title": "New task title",
    "description": "Task description (optional)",
    "completed": false
  }
  ```
- **Response Success (201)**:
  ```json
  {
    "id": "task-uuid",
    "title": "New task title",
    "description": "Task description (optional)",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "user_id": "user-uuid"
  }
  ```
- **Response Errors**: 400 (validation), 401 (invalid/missing token), 500 (server error)

#### GET /api/tasks/{task_id}
- **Auth Required**: Yes
- **Purpose**: Get a specific task for authenticated user
- **Path Parameter**: `task_id` (UUID of the task)
- **Response Success (200)**:
  ```json
  {
    "id": "task-uuid",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "user_id": "user-uuid"
  }
  ```
- **Response Errors**: 401 (invalid/missing token), 403 (not owner), 404 (task not found), 500 (server error)

#### PUT /api/tasks/{task_id}
- **Auth Required**: Yes
- **Purpose**: Update a specific task for authenticated user
- **Path Parameter**: `task_id` (UUID of the task)
- **Request Body**:
  ```json
  {
    "title": "Updated task title (optional)",
    "description": "Updated description (optional)",
    "completed": true
  }
  ```
- **Response Success (200)**:
  ```json
  {
    "id": "task-uuid",
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z",
    "user_id": "user-uuid"
  }
  ```
- **Response Errors**: 400 (validation), 401 (invalid/missing token), 403 (not owner), 404 (task not found), 500 (server error)

#### DELETE /api/tasks/{task_id}
- **Auth Required**: Yes
- **Purpose**: Delete a specific task for authenticated user
- **Path Parameter**: `task_id` (UUID of the task)
- **Response Success (200)**:
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```
- **Response Errors**: 401 (invalid/missing token), 403 (not owner), 404 (task not found), 500 (server error)

## Request/Response Schemas

### Common Request Headers
- `Authorization: Bearer <jwt-token>` (for protected endpoints)
- `Content-Type: application/json` (for POST/PUT requests)
- `Accept: application/json`

### Common Response Headers
- `Content-Type: application/json`
- `X-Request-ID: <uuid>` (for request tracking)

### Common Error Response Schema
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Optional field-specific error details
    }
  }
}
```

### Success Response Schema
```json
{
  "data": {
    // Response data
  },
  "message": "Optional success message"
}
```

## Error Responses

### 400 Bad Request
- **Cause**: Invalid request format, missing required fields, validation errors
- **Response**:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Request validation failed",
      "details": {
        "field_name": "Error message for specific field"
      }
    }
  }
  ```

### 401 Unauthorized
- **Cause**: Missing, invalid, or expired JWT token
- **Response**:
  ```json
  {
    "error": {
      "code": "UNAUTHORIZED",
      "message": "Authentication required or token invalid"
    }
  }
  ```

### 403 Forbidden
- **Cause**: User trying to access resource they don't own
- **Response**:
  ```json
  {
    "error": {
      "code": "FORBIDDEN",
      "message": "Access to this resource is forbidden"
    }
  }
  ```

### 404 Not Found
- **Cause**: Requested resource doesn't exist
- **Response**:
  ```json
  {
    "error": {
      "code": "NOT_FOUND",
      "message": "The requested resource was not found"
    }
  }
  ```

### 429 Too Many Requests
- **Cause**: Rate limit exceeded
- **Response**:
  ```json
  {
    "error": {
      "code": "RATE_LIMIT_EXCEEDED",
      "message": "Too many requests, please try again later"
    }
  }
  ```

### 500 Internal Server Error
- **Cause**: Unexpected server error
- **Response**:
  ```json
  {
    "error": {
      "code": "INTERNAL_ERROR",
      "message": "An unexpected error occurred"
    }
  }
  ```

## Ownership Enforcement Rules

### General Ownership Rules
- **OWN-001**: All protected endpoints MUST verify user owns the resource being accessed
- **OWN-002**: Database queries MUST filter by authenticated user ID
- **OWN-003**: Resource creation MUST assign resource to authenticated user
- **OWN-004**: Resource modification MUST verify user is the resource owner
- **OWN-005**: Resource deletion MUST verify user is the resource owner

### Task-Specific Ownership Rules
- **OWN-006**: Users can only read their own tasks (GET /api/tasks and GET /api/tasks/{id})
- **OWN-007**: Users can only update their own tasks (PUT /api/tasks/{id})
- **OWN-008**: Users can only delete their own tasks (DELETE /api/tasks/{id})
- **OWN-009**: Task creation automatically assigns task to authenticated user (user_id field)
- **OWN-010**: All task queries MUST include user_id filter in WHERE clause
- **OWN-011**: If task doesn't belong to authenticated user, return 403 Forbidden
- **OWN-012**: Task ownership check MUST happen after JWT validation but before business logic