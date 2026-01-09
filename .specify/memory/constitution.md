<!--
Sync Impact Report:
Version change: 0.1.0 → 1.0.0
Added sections: Spec-Driven Development, Security Boundaries, Technical Stack, API Rules, Database Rules
Removed sections: None
Modified principles: All principles updated to reflect hackathon-todo project requirements
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# hackathon-todo Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All implementation work MUST be based on approved specifications; No code implementation without a corresponding spec; All features must have user stories and acceptance criteria defined before development begins; Specifications must be reviewed and approved by stakeholders before implementation starts.

### II. Security-First Architecture
Security is a primary concern in all design decisions; Authentication and authorization must be implemented correctly at all layers; Never trust user input without validation; All API endpoints must enforce proper authentication and authorization; Sensitive data must be handled according to security best practices.

### III. Test-First Development (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced; All features must have unit, integration, and end-to-end tests; Code coverage must meet minimum thresholds defined in the project standards.

### IV. Frontend-Backend Separation
Clear separation of concerns between frontend and backend responsibilities; Frontend handles UI/UX and client-side logic; Backend provides API services and business logic; Communication happens exclusively through well-defined API contracts; No direct database access from frontend.

### V. Authentication and Authorization Integrity
Better Auth runs ONLY in frontend; Backend must NEVER trust user_id from URL without JWT validation; JWT must be verified using shared secret (BETTER_AUTH_SECRET); Every API request must include Authorization: Bearer <token>; Backend extracts user identity ONLY from JWT; Backend enforces task ownership on every operation.

### VI. API-First Design


All APIs must follow RESTful conventions; APIs must be documented with clear contracts; Versioning strategy must be implemented for all public APIs; API security rules must be strictly enforced; JSON only for request/response payloads.

## Security Boundaries and Responsibilities

### Frontend vs Backend Responsibilities
- Frontend: User interface, client-side validation, Better Auth integration, JWT token management
- Backend: Data validation, business logic, database operations, JWT verification, authentication enforcement
- Shared: API contracts, error handling standards, security headers

### Authentication Model
- Better Auth handles user registration, login, and session management on frontend
- JWT tokens are issued by Better Auth and validated by backend
- Shared secret (BETTER_AUTH_SECRET) used for JWT verification
- Stateful session management on frontend, stateless authentication on backend
- Password hashing and storage handled by Better Auth

### Database Ownership and Access Rules
- users table is managed logically by Better Auth
- tasks table must reference users.id for proper ownership
- All database queries must be filtered by authenticated user
- Direct database access from frontend is prohibited
- Backend enforces row-level security based on user authentication

## Technical Stack Requirements

### Mandatory Technologies
- Frontend: Next.js 16+ (App Router, TypeScript, Tailwind CSS)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (frontend) with JWT tokens
- Authorization: JWT verification in FastAPI
- Spec System: Spec-Kit Plus

### Coding Standards and Conventions
- TypeScript for all frontend code with strict typing
- Python type hints for all backend functions
- Consistent naming conventions across frontend and backend
- Comprehensive documentation for all public APIs
- Code linting and formatting enforced via project configuration
- Commit messages follow conventional commit format

## API Security Rules

### Endpoint Requirements
- All routes under /api/ namespace
- RESTful conventions with proper HTTP methods
- JSON only for request/response payloads
- Stateless authentication required
- Return 401 for missing/invalid tokens
- Return 403 for unauthorized access attempts
- Rate limiting implemented for all endpoints
- Input validation required for all parameters

### Authentication Enforcement
- Authorization: Bearer <token> header required for all protected endpoints
- JWT token validation must occur before processing requests
- Token expiration must be handled gracefully
- Refresh token mechanism must be properly implemented
- Session management follows security best practices

## Database Rules

### Schema Requirements
- users table managed by Better Auth (logical ownership)
- tasks table must have foreign key reference to users.id
- All queries must be filtered by authenticated user
- Proper indexing for performance and security
- Database migrations must be versioned and reversible

### Access Control
- Row-level security based on user authentication
- No direct database access from frontend
- Backend enforces proper ownership checks
- Audit logging for sensitive operations
- Data retention and privacy compliance

## Spec Rules

### Specification Requirements
- All features must have user stories describing user needs
- Acceptance criteria must be specific, measurable, and testable
- Specifications must include security and performance considerations
- API contracts must be defined before implementation
- Database schema changes must be documented in specs

### Quality Standards
- Specifications must be reviewed and approved before implementation
- Changes to specs require proper approval process
- Specifications must align with overall project architecture
- User stories must follow standard format and structure
- Acceptance criteria must be verifiable through testing

## Development Workflow

### Code Review Process
- All code changes require peer review
- Security implications must be considered in reviews
- Tests must pass before code is merged
- Specifications must be referenced in pull requests
- Documentation updates required for all significant changes

### Quality Gates
- All automated tests must pass
- Code coverage requirements must be met
- Security scanning must pass
- Performance benchmarks must be maintained
- Specification compliance must be verified

## Governance

### Amendment Process
- Constitution amendments require team consensus and stakeholder approval
- Changes must be documented with rationale and impact assessment
- All affected templates and documentation must be updated
- Team members must acknowledge new version of constitution
- Version control tracks all changes with proper commit messages

### Compliance Review
- Regular constitution compliance reviews must be conducted
- All pull requests must verify constitution compliance
- Violations must be addressed before merge
- Exception process available for special circumstances with proper approval
- Constitution adherence is part of developer onboarding

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06
