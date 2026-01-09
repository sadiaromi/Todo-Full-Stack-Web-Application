# Architecture Specification: Full-Stack Todo Web Application

## Frontend/Backend Separation
The application follows a modern web architecture with clear separation between frontend and backend:

- **Frontend**: Next.js/React application running in the browser
  - Handles user interface and user interactions
  - Manages client-side state and routing
  - Makes API calls to the backend
  - Stores JWT tokens in browser storage

- **Backend**: FastAPI application running on a server
  - Exposes RESTful API endpoints
  - Handles business logic and data validation
  - Interacts with the database
  - Manages authentication and authorization

## Auth Flow (Better Auth → JWT → FastAPI)
The authentication flow follows this sequence:

1. **User Registration/Login**:
   - User submits credentials via Better Auth
   - Better Auth validates credentials against database
   - Better Auth generates JWT token with user identity
   - Token is returned to frontend and stored in browser

2. **Authenticated API Requests**:
   - Frontend includes JWT token in Authorization header
   - FastAPI middleware validates JWT token
   - User identity is extracted from token payload
   - Request is processed with user context

3. **Token Expiration**:
   - JWT tokens have configurable expiration time
   - Upon expiration, user must re-authenticate
   - Frontend detects 401 responses and redirects to login

## Request Lifecycle
1. **Client Request**: User performs action in browser
2. **API Call**: Frontend makes HTTP request to backend with JWT token
3. **Authentication**: FastAPI validates JWT token and extracts user ID
4. **Authorization**: Backend verifies user has permission to perform action
5. **Processing**: Business logic is executed
6. **Database**: Data operations performed with user context
7. **Response**: Result returned to frontend
8. **UI Update**: Frontend updates interface based on response

## Security Boundaries
- **Network Boundary**: All API requests must go through /api/ endpoints
- **Authentication Boundary**: JWT tokens required for all protected endpoints
- **Authorization Boundary**: User can only access/modify their own data
- **Data Boundary**: Database queries are filtered by authenticated user ID
- **Input Boundary**: All user input is validated before processing

## Data Flow Diagram (Textual)

```
+-------------------+     HTTP Request     +------------------+
|                   |  +---------------+   |                  |
|   Frontend        |  | Authorization |   |    Backend       |
|   (Next.js)       |  | Header:       |   |    (FastAPI)     |
|                   |  | Bearer <JWT>  |   |                  |
+--------+----------+  +---------------+   +---------+--------+
         |                                       |
         | (1) API Request with JWT              | (2) Validate JWT
         +---------------------------------------> and extract user
                                                 |
         +---------------------------------------+
         | (3) Process request with user context |
         | (4) Query database with user filter   |
         | (5) Return response                   |
         |
         | (6) Update UI based on response
         +---------------------------------------+
         |
+--------+----------+                           +---------+--------+
|                   |                           |                  |
|   Browser         |<--------------------------|   Database       |
|   Storage         |   (7) Store tokens        |   (PostgreSQL)   |
|   (JWT)           |   for future requests     |                  |
+-------------------+                           +------------------+
```

## Technology Components

### Frontend Stack
- **Framework**: Next.js 14+ with React
- **Authentication**: Better Auth client library
- **State Management**: React state/hooks and context
- **Styling**: Tailwind CSS or similar
- **API Client**: Built-in fetch or axios

### Backend Stack
- **Framework**: FastAPI
- **Authentication**: JWT token validation
- **Database ORM**: SQLAlchemy or similar
- **Authentication Provider**: Better Auth integration
- **Environment**: Python 3.9+

### Database Schema
- **users** table: Stores user information
- **tasks** table: Stores user tasks with foreign key to users
- **indexes**: On user_id for efficient querying
- **constraints**: Foreign key relationships and data validation

## Deployment Architecture
- **Frontend**: Static hosting (Vercel, Netlify, etc.)
- **Backend**: API server with reverse proxy
- **Database**: Managed PostgreSQL service
- **Authentication**: Better Auth service or self-hosted
- **Security**: HTTPS required for all communication