# Full-Stack Todo Web Application

A full-stack todo application built with Next.js, FastAPI, and PostgreSQL, featuring secure user authentication and task management.

## Features

- User authentication (signup, login, logout)
- JWT-based authentication with refresh tokens
- Task management (create, read, update, delete)
- Task filtering by completion status
- Secure API endpoints with proper authorization
- Rate limiting for authentication endpoints

## Tech Stack

- **Frontend**: Next.js 14+, React
- **Backend**: FastAPI 0.104+
- **Database**: PostgreSQL
- **Authentication**: JWT with refresh tokens
- **ORM**: SQLModel (SQLAlchemy + Pydantic)

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL 12+

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```


```

### Running the Application

1. Start the backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

The application will be available at `http://localhost:3000`.

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Authenticate user
- `POST /api/auth/logout` - Logout user

### Tasks
- `GET /api/tasks` - Get user's tasks (with optional status filter)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get specific task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task

## Security Features

- JWT token validation on all protected endpoints
- User ID extracted from JWT, not from URL parameters
- Ownership enforcement on all task operations
- Rate limiting: 5 failed attempts per 15 minutes per IP/user
- Password strength validation (8+ chars, upper, lower, number, special char)
- Input validation (task title: max 100 chars, description: max 1000 chars)

## Architecture

The application follows a clean architecture with clear separation between frontend and backend:

- **Frontend**: Next.js/React application with Better Auth integration
- **Backend**: FastAPI application with SQLModel for database operations
- **Database**: PostgreSQL with proper relationships
- **Authentication**: JWT-based with refresh tokens
- **Security**: Token validation, ownership enforcement, rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.
