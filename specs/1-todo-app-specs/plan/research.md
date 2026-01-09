# Research Document: Full-Stack Todo Web Application

## 0.1 Better Auth Integration Research
- **Decision**: Use Better Auth with JWT for frontend authentication
- **Rationale**: Provides secure authentication with built-in best practices
- **Implementation**: Install better-auth package and configure with Next.js
- **Alternatives considered**:
  - Auth.js: More complex setup, more manual configuration
  - Clerk: More expensive for open-source projects
  - Custom JWT: More security risk, more development time

## 0.2 FastAPI JWT Middleware Research
- **Decision**: Implement custom JWT middleware for token validation
- **Rationale**: Provides consistent authentication across all protected endpoints
- **Implementation**: Create middleware that validates JWT and extracts user_id
- **Alternatives considered**:
  - python-jose: More dependencies, similar functionality
  - PyJWT: More manual implementation needed
  - FastAPI's built-in OAuth2: Doesn't fit our specific JWT requirements

## 0.3 SQLModel Database Design Research
- **Decision**: Use SQLModel for database models with proper relationships
- **Rationale**: Combines SQLAlchemy and Pydantic for type safety
- **Implementation**: Define User and Task models with proper constraints
- **Alternatives considered**:
  - SQLAlchemy alone: Missing Pydantic integration for API validation
  - Tortoise ORM: Async-only, doesn't fit our FastAPI sync patterns well
  - Peewee: Less type safety, less integration with FastAPI

## 0.4 Refresh Token Strategy Research
- **Decision**: Implement refresh token rotation for enhanced security
- **Rationale**: Provides seamless user experience while maintaining security
- **Implementation**: Issue short-lived access tokens with longer refresh tokens
- **Alternatives considered**:
  - Session-based storage: More complex for our API-first approach
  - Long-lived JWT tokens: Security risk with no way to revoke
  - No refresh tokens: Poor user experience with frequent re-authentication