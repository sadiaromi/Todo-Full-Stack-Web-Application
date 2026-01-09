# Data Model: Full-Stack Todo Web Application

## User Entity

### Fields
- **id**: UUID (Primary Key, Required)
  - Auto-generated UUID
  - Unique identifier for each user
- **email**: String (Required, Unique, Max 255 chars)
  - User's email address for authentication
  - Must be unique across all users
- **password_hash**: String (Required, Max 255 chars)
  - Bcrypt hash of the user's password
  - Never store plain text passwords
- **created_at**: DateTime (Required, Default: now)
  - Timestamp when the user account was created
- **updated_at**: DateTime (Required, Default: now)
  - Timestamp when the user record was last updated

### Relationships
- **tasks**: One-to-Many relationship to Task entity
  - A user can have zero or more tasks
  - When user is deleted, all their tasks are also deleted (CASCADE)

### Validation Rules
- Email must follow standard email format
- Email must be unique
- Password hash must be present
- Email must not be empty

## Task Entity

### Fields
- **id**: UUID (Primary Key, Required)
  - Auto-generated UUID
  - Unique identifier for each task
- **user_id**: UUID (Required, Foreign Key to users.id)
  - References the user who owns this task
  - Enforces ownership relationship
- **title**: String (Required, Max 100 chars)
  - Title of the task (from spec clarification)
  - Required field for all tasks
- **description**: String (Optional, Max 1000 chars)
  - Detailed description of the task (from spec clarification)
  - Can be null/empty
- **completed**: Boolean (Required, Default: false)
  - Indicates whether the task is completed
  - Used for filtering and UI display
- **created_at**: DateTime (Required, Default: now)
  - Timestamp when the task was created
- **updated_at**: DateTime (Required, Default: now)
  - Timestamp when the task was last updated

### Relationships
- **user**: Many-to-One relationship to User entity
  - Each task belongs to exactly one user
  - Enforces ownership at database level

### Validation Rules
- Title must be present and not empty
- Title must be 100 characters or less
- Description must be 1000 characters or less (if present)
- User_id must reference a valid user
- Completed field must be a boolean value

## Constraints

### Primary Key Constraints
- Both User and Task entities have UUID primary keys
- Primary keys are auto-generated using UUID4

### Foreign Key Constraints
- Task.user_id references User.id
- ON DELETE CASCADE: When a user is deleted, all their tasks are also deleted
- Ensures referential integrity at database level

### Unique Constraints
- User.email must be unique across all users
- Prevents duplicate account creation

### Check Constraints
- No explicit check constraints needed beyond field validations
- Application-level validation handles additional business rules

## Indexes

### Required Indexes
- **idx_tasks_user_id**: On Task.user_id for efficient ownership queries
  - Critical for enforcing user access to their own tasks
  - Improves performance of user-specific queries
- **idx_tasks_completed**: On Task.completed for efficient status filtering
  - Improves performance of completed/incomplete task queries
- **idx_tasks_created_at**: On Task.created_at for time-based queries
  - Improves performance of date range queries
- **idx_tasks_user_completed**: Composite index on (user_id, completed)
  - Optimizes common queries filtering by both user and status

## State Transitions

### Task State Transitions
- **Active** → **Completed**: When user marks task as complete
  - completed field changes from false to true
  - updated_at field is updated to current timestamp
- **Completed** → **Active**: When user marks task as incomplete
  - completed field changes from true to false
  - updated_at field is updated to current timestamp

### User State Transitions
- **New User** → **Active**: When user completes signup
  - Account is created with provided email and hashed password
- **Active** → **Deleted**: When user account is deleted
  - Account and all associated tasks are removed (due to CASCADE)

## Data Lifecycle

### Creation
- User accounts are created during signup process
- Tasks are created when users add new tasks to their list
- Creation timestamps are automatically set

### Updates
- User records updated when account information changes
- Task records updated when task details change
- Update timestamps are automatically updated

### Deletion
- User deletion triggers CASCADE deletion of all associated tasks
- Individual tasks can be deleted by the task owner
- Deletion follows the ownership enforcement rules

## Security Considerations

### Data Protection
- Passwords stored as bcrypt hashes, never plain text
- User identity stored in JWT tokens for session management
- All database queries filtered by authenticated user ID

### Access Control
- Foreign key relationships enforce ownership at database level
- Application logic must validate user permissions before database operations
- Row-level security implemented through user_id filtering