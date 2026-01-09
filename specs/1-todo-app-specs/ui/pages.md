# UI Pages Specification: Todo Application

## Login Page

### Purpose
Page where existing users can authenticate with their credentials to access their todo lists.

### Components
- **AuthForm** component in login mode
- **Header** component (without user controls since not logged in)
- **Footer** component with app information

### Layout
- Centered authentication form
- App branding/logo at top
- Login form with email and password fields
- "Don't have an account? Sign up" link
- Error message display area

### Behavior
- **BP-001**: Shows login form by default
- **BP-002**: On successful login, redirects to dashboard
- **BP-003**: On authentication error, displays error message
- **BP-004**: "Sign up" link navigates to signup page
- **BP-005**: Form shows loading state during submission
- **BP-006**: Page redirects to dashboard if user is already logged in

### Acceptance Criteria
- **AC-001**: User can enter email and password
- **AC-002**: Form validates required fields
- **AC-003**: User is redirected to dashboard after successful login
- **AC-004**: Error messages are displayed for invalid credentials
- **AC-005**: User can navigate to signup page from login page
- **AC-006**: Already authenticated users are redirected from this page

## Signup Page

### Purpose
Page where new users can create accounts to start using the todo application.

### Components
- **AuthForm** component in signup mode
- **Header** component (without user controls since not logged in)
- **Footer** component with app information

### Layout
- Centered authentication form
- App branding/logo at top
- Signup form with email and password fields
- "Already have an account? Log in" link
- Error message display area

### Behavior
- **BP-007**: Shows signup form by default
- **BP-008**: On successful signup, redirects to dashboard
- **BP-009**: On validation error, displays error message
- **BP-010**: "Log in" link navigates to login page
- **BP-011**: Form shows loading state during submission
- **BP-012**: Page redirects to dashboard if user is already logged in

### Acceptance Criteria
- **AC-007**: User can enter email and password
- **AC-008**: Form validates email format and password strength
- **AC-009**: User is redirected to dashboard after successful signup
- **AC-010**: Error messages are displayed for validation failures
- **AC-011**: User can navigate to login page from signup page
- **AC-012**: Already authenticated users are redirected from this page

## Dashboard Page

### Purpose
Main application page where authenticated users can view and manage their tasks.

### Components
- **Header** component with user controls
- **TaskForm** component for creating new tasks
- **TaskCard** components for existing tasks
- **Filter controls** for task status
- **LoadingSpinner** when tasks are loading
- **ErrorMessage** for API errors

### Layout
- Header with app title and user controls
- Task creation form at top
- Filter controls (show all/completed/incomplete)
- Task list with individual task cards
- Empty state message when no tasks exist

### Behavior
- **BP-013**: Loads and displays user's tasks on page load
- **BP-014**: Shows loading state while fetching tasks
- **BP-015**: Allows creating new tasks via form
- **BP-016**: Updates task list after create/update/delete operations
- **BP-017**: Filters tasks based on completion status
- **BP-018**: Shows empty state when user has no tasks

### Acceptance Criteria
- **AC-013**: Authenticated user can view their tasks
- **AC-014**: User can create new tasks
- **AC-015**: User can update task completion status
- **AC-016**: User can filter tasks by completion status
- **AC-017**: User can see loading state during operations
- **AC-018**: Proper error handling for API failures

## Task List Page

### Purpose
Alternative view for users who prefer to see their tasks in a dedicated list format.

### Components
- **Header** component with user controls
- **TaskCard** components for all tasks
- **Filter controls** for task status
- **Pagination controls** for large task lists
- **LoadingSpinner** when tasks are loading

### Layout
- Header with navigation
- Filter controls at top
- Task list with cards
- Pagination controls at bottom
- Empty state message when no tasks match filters

### Behavior
- **BP-019**: Loads user's tasks with optional filtering
- **BP-020**: Supports pagination for large task sets
- **BP-021**: Updates in real-time when tasks change
- **BP-022**: Maintains filter state across navigation
- **BP-023**: Shows loading state during data operations

### Acceptance Criteria
- **AC-019**: User can view all tasks in list format
- **AC-020**: Tasks can be filtered by completion status
- **AC-021**: Pagination works for large task lists
- **AC-022**: Task updates reflect immediately in list
- **AC-023**: Loading states are properly displayed

## Create/Edit Task Page

### Purpose
Dedicated page for creating new tasks or editing existing ones with more detailed controls.

### Components
- **Header** component with user controls
- **TaskForm** component with full editing capabilities
- **CancelButton** to return to dashboard

### Layout
- Header with navigation
- Full task form with all fields
- Action buttons (Save, Cancel)
- Error message display area

### Behavior
- **BP-024**: Shows empty form for creating new tasks
- **BP-025**: Shows pre-filled form for editing existing tasks
- **BP-026**: Validates form before submission
- **BP-027**: Redirects to dashboard after successful save
- **BP-028**: Returns to dashboard when cancel is clicked

### Acceptance Criteria
- **AC-024**: User can create detailed tasks with all fields
- **AC-025**: User can edit existing tasks with all fields
- **AC-026**: Form validates required fields before submission
- **AC-027**: Successful saves redirect to dashboard
- **AC-028**: Cancel action returns to previous page

## Protected Routes Behavior

### Authentication Enforcement
- **PR-001**: Unauthenticated users attempting to access protected pages MUST be redirected to login
- **PR-002**: Protected routes include: dashboard, task list, create/edit task
- **PR-003**: Redirect MUST preserve intended destination for post-login navigation
- **PR-004**: Authentication status MUST be checked on initial page load and route changes

### JWT Token Handling
- **PR-005**: Application MUST check for valid JWT token before rendering protected content
- **PR-006**: Expired tokens MUST trigger redirect to login page
- **PR-007**: Invalid tokens MUST trigger redirect to login page
- **PR-008**: Token refresh (if implemented) SHOULD happen transparently

### Error Handling for Protected Routes
- **PR-009**: Network errors during authentication checks SHOULD show appropriate messaging
- **PR-010**: Server errors during authentication checks SHOULD redirect to login
- **PR-011**: Session timeout during usage SHOULD redirect to login with warning message
- **PR-012**: Failed API calls due to authentication SHOULD trigger re-authentication flow

### User Experience Considerations
- **PR-013**: Protected routes SHOULD show loading state while checking authentication
- **PR-014**: Navigation SHOULD be smooth between protected pages for authenticated users
- **PR-015**: Error states SHOULD be handled gracefully without breaking navigation
- **PR-016**: User's intended destination SHOULD be preserved across authentication redirects

### Session Management
- **PR-017**: Application MUST detect when user session becomes invalid
- **PR-018**: Invalid session detection SHOULD occur on API response with 401 status
- **PR-019**: Automatic logout SHOULD clear all user data and tokens
- **PR-020**: User SHOULD be notified when automatic logout occurs