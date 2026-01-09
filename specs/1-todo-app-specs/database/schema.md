# Database Schema Specification: Todo Application

## Users Table
The users table stores information about registered users of the application.

### Table Definition
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Column Descriptions
- **id**: Primary key, universally unique identifier for the user
  - Type: UUID
  - Constraints: PRIMARY KEY, DEFAULT gen_random_uuid()
  - Purpose: Unique identifier for each user, used as foreign key reference

- **email**: User's email address used for authentication
  - Type: VARCHAR(255)
  - Constraints: UNIQUE, NOT NULL
  - Purpose: User's login identifier and primary contact method

- **password_hash**: Bcrypt hash of the user's password
  - Type: VARCHAR(255)
  - Constraints: NOT NULL
  - Purpose: Securely stored password hash (never store plain text passwords)

- **created_at**: Timestamp when the user account was created
  - Type: TIMESTAMP WITH TIME ZONE
  - Constraints: DEFAULT CURRENT_TIMESTAMP
  - Purpose: Track account creation time for auditing and analytics

- **updated_at**: Timestamp when the user record was last updated
  - Type: TIMESTAMP WITH TIME ZONE
  - Constraints: DEFAULT CURRENT_TIMESTAMP
  - Purpose: Track last modification time for the user record

## Tasks Table
The tasks table stores todo items created by users.

### Table Definition
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Column Descriptions
- **id**: Primary key, universally unique identifier for the task
  - Type: UUID
  - Constraints: PRIMARY KEY, DEFAULT gen_random_uuid()
  - Purpose: Unique identifier for each task

- **user_id**: Foreign key reference to the user who owns the task
  - Type: UUID
  - Constraints: NOT NULL, FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE
  - Purpose: Establishes ownership relationship between task and user

- **title**: Title or brief description of the task
  - Type: VARCHAR(255)
  - Constraints: NOT NULL
  - Purpose: Human-readable title for the task

- **description**: Detailed description of the task (optional)
  - Type: TEXT
  - Constraints: None (NULLable)
  - Purpose: Additional details about what needs to be done

- **completed**: Boolean indicating whether the task is completed
  - Type: BOOLEAN
  - Constraints: DEFAULT FALSE
  - Purpose: Track task completion status

- **created_at**: Timestamp when the task was created
  - Type: TIMESTAMP WITH TIME ZONE
  - Constraints: DEFAULT CURRENT_TIMESTAMP
  - Purpose: Track task creation time

- **updated_at**: Timestamp when the task was last updated
  - Type: TIMESTAMP WITH TIME ZONE
  - Constraints: DEFAULT CURRENT_TIMESTAMP
  - Purpose: Track last modification time for the task

## Relationships

### User-Task Relationship
- **Type**: One-to-Many (One user can have many tasks)
- **Implementation**: Foreign key (user_id) in tasks table references users(id)
- **Constraint**: ON DELETE CASCADE - when a user is deleted, all their tasks are automatically deleted
- **Purpose**: Enforce data integrity and ownership relationships

### Relationship Constraints
- **RC-001**: Each task MUST be associated with exactly one user
- **RC-002**: Each user MAY have zero or more tasks
- **RC-003**: When a user account is deleted, all associated tasks are automatically deleted
- **RC-004**: Attempt to create task with non-existent user_id MUST fail with constraint violation
- **RC-005**: All queries for tasks MUST be filtered by user_id to enforce ownership

## Indexes

### Required Indexes
```sql
-- Index for user_id to optimize user-specific queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for completed status to optimize status-based queries
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Index for created_at to optimize time-based queries
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Composite index for user and status to optimize common filtered queries
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

### Index Purposes
- **idx_tasks_user_id**: Optimize queries filtering tasks by user (essential for ownership enforcement)
- **idx_tasks_completed**: Optimize queries filtering tasks by completion status
- **idx_tasks_created_at**: Optimize queries with time-based filtering or sorting
- **idx_tasks_user_completed**: Optimize common queries that filter by both user and status

## Constraints

### Primary Key Constraints
- **PK-001**: Both tables MUST have primary key constraints (id fields)
- **PK-002**: Primary key values MUST be unique and non-null
- **PK-003**: Primary keys are auto-generated using UUID

### Foreign Key Constraints
- **FK-001**: tasks.user_id MUST reference valid users.id
- **FK-002**: Foreign key relationship enforces referential integrity
- **FK-003**: ON DELETE CASCADE ensures data consistency when users are removed

### Uniqueness Constraints
- **UC-001**: users.email MUST be unique to prevent duplicate accounts
- **UC-002**: No additional uniqueness constraints needed for tasks table

### Check Constraints
- **CC-001**: users.email MUST follow standard email format (application-level validation)
- **CC-002**: tasks.title MUST NOT be empty or only whitespace (application-level validation)

### Not Null Constraints
- **NN-001**: users.email and users.password_hash MUST NOT be null
- **NN-002**: tasks.user_id and tasks.title MUST NOT be null
- **NN-003**: All primary key fields MUST NOT be null
- **NN-004**: created_at and updated_at will have defaults but could be null in edge cases

## Security Considerations

### Data Protection
- **SEC-001**: Passwords MUST be stored as bcrypt hashes, never plain text
- **SEC-002**: No sensitive authentication data other than password hashes should be stored
- **SEC-003**: All database connections MUST use encrypted connections (SSL/TLS)

### Access Control
- **SEC-004**: Database queries MUST always filter by user_id to enforce ownership
- **SEC-005**: Direct database access SHOULD be restricted to application layer
- **SEC-006**: Row-level security SHOULD be implemented at database level as additional protection

### Audit Requirements
- **SEC-007**: created_at and updated_at fields provide basic audit trail
- **SEC-008**: Additional audit logging MAY be implemented for security events
- **SEC-009**: User account creation and modification times are tracked

## Performance Considerations

### Query Optimization
- **PERF-001**: Indexes on user_id are critical for ownership-based queries
- **PERF-002**: Composite indexes support common query patterns
- **PERF-003**: UUID primary keys provide distributed system compatibility
- **PERF-004**: Default timestamps eliminate need for application-level time setting

### Scalability
- **SCAL-001**: UUID primary keys support horizontal scaling
- **SCAL-002**: Proper indexing supports efficient querying as data grows
- **SCAL-003**: Foreign key constraints maintain data integrity at scale