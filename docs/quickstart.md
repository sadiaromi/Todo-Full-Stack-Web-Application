# Quickstart Guide: Full-Stack Todo Web Application

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.9+ for backend development
- PostgreSQL 12+ for database
- Git for version control

## Environment Setup

### Backend Environment Variables

Create a `.env` file in the backend directory:

```bash
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/todo_app"

# JWT Configuration
JWT_SECRET="your-super-secret-jwt-key-here-make-it-long-and-random"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Better Auth Configuration
BETTER_AUTH_SECRET="your-better-auth-secret"
BETTER_AUTH_URL="http://localhost:3000"

# Application Configuration
API_PREFIX="/api"
DEBUG_MODE=true
```

### Frontend Environment Variables

Create a `.env.local` file in the frontend directory:

```bash
# Backend API Configuration
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_BASE_URL="http://localhost:3000"

# Better Auth Configuration
BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_SECRET="your-better-auth-secret"
```

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Required packages in `requirements.txt`:
```
fastapi==0.104.1
sqlmodel==0.0.8
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
psycopg2-binary==2.9.9
pydantic==2.5.0
```

### 2. Initialize Database

```bash
# Run database migrations
python -m backend.app.database.init_db

# Or using alembic if using migrations
alembic upgrade head
```

### 3. Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

### 1. Install Node Dependencies

```bash
cd frontend
npm install
```

### 2. Start Frontend Development Server

```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Authenticate user
- `POST /api/auth/logout` - Logout user

### Task Management Endpoints

- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get specific task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task

## Running Tests

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Development Workflow

1. **Start Database**: Ensure PostgreSQL is running
2. **Start Backend**: Run backend server on port 8000
3. **Start Frontend**: Run frontend dev server on port 3000
4. **Access Application**: Visit http://localhost:3000

## Key Implementation Notes

### Security Considerations
- All API requests must include `Authorization: Bearer <token>` header
- User ID is extracted from JWT token, never from URL parameters
- All database queries are filtered by authenticated user ID
- Passwords are hashed using bcrypt with salt

### Error Handling
- 401 responses for invalid/missing tokens
- 403 responses for unauthorized access attempts
- 404 responses for non-existent resources
- 400 responses for validation errors

### Data Validation
- Task titles: maximum 100 characters
- Task descriptions: maximum 1000 characters
- Passwords: minimum 8 characters with uppercase, lowercase, number, and special character
- Rate limiting: 5 failed attempts per 15 minutes per IP/user

## Deployment

### Production Environment Variables

For production, ensure these environment variables are set securely:

```bash
# Use strong, unique values for production
JWT_SECRET="production-jwt-secret-here"
DATABASE_URL="postgresql://prod-user:prod-password@prod-db:5432/todo_app_prod"
DEBUG_MODE=false
```

### Docker Deployment

Example `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/todo_app
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=todo_app
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```