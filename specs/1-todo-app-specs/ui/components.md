# UI Components Specification: Todo Application

## Reusable Components

### Header Component
- **Purpose**: Consistent application header with navigation and user controls
- **Props**:
  - `isLoggedIn`: Boolean indicating user authentication status
  - `userEmail`: String with user's email (when logged in)
  - `onLogout`: Function to handle logout action
- **Features**:
  - Display app logo/title
  - Show user email when logged in
  - Show logout button when logged in
  - Show login/signup links when not logged in
- **Acceptance**: Header appears consistently across all pages

### TaskCard Component
- **Purpose**: Display individual task information with action controls
- **Props**:
  - `task`: Object containing task data (id, title, description, completed)
  - `onToggleComplete`: Function to handle completion toggle
  - `onEdit`: Function to handle edit action
  - `onDelete`: Function to handle delete action
- **Features**:
  - Display task title with visual indication of completion status
  - Show task description if available
  - Show completion checkbox that toggles task status
  - Show edit and delete buttons
  - Visual feedback when task is completed (strikethrough, color change)
- **Acceptance**: Task is visually distinct when completed, actions work as expected

### TaskForm Component
- **Purpose**: Form for creating and editing tasks
- **Props**:
  - `initialData`: Object with initial form values (optional, for editing)
  - `onSubmit`: Function to handle form submission
  - `onCancel`: Function to handle cancel action (optional)
- **Features**:
  - Input field for task title (required)
  - Textarea for task description (optional)
  - Checkbox for completion status
  - Submit button with validation
  - Cancel button (when editing)
  - Form validation with error messages
- **Acceptance**: Form validates required fields, submits properly formatted data

### AuthForm Component
- **Purpose**: Reusable form for authentication (login or signup)
- **Props**:
  - `mode`: String indicating "login" or "signup"
  - `onSubmit`: Function to handle form submission
  - `onSwitchMode`: Function to switch between login/signup
- **Features**:
  - Email input field with validation
  - Password input field with strength requirements (signup)
  - Submit button with loading state
  - Link to switch between login/signup modes
  - Error message display
- **Acceptance**: Form validates inputs, handles authentication flows

## Forms

### Signup Form
- **Fields**:
  - Email (required, validated format)
  - Password (required, minimum 8 characters, strength requirements)
- **Validation**:
  - Email format validation
  - Password strength requirements
  - Required field validation
  - Duplicate email detection
- **Behavior**:
  - Shows loading state during submission
  - Displays error messages for validation failures
  - Redirects to dashboard on success
- **Acceptance**: User can create account with valid credentials, errors shown for invalid inputs

### Login Form
- **Fields**:
  - Email (required)
  - Password (required)
- **Validation**:
  - Email format validation
  - Required field validation
  - Authentication validation
- **Behavior**:
  - Shows loading state during submission
  - Displays error messages for authentication failures
  - Redirects to dashboard on success
- **Acceptance**: User can log in with valid credentials, errors shown for invalid inputs

### Task Creation Form
- **Fields**:
  - Title (required, max 255 characters)
  - Description (optional, text area)
- **Validation**:
  - Title required validation
  - Title length validation
- **Behavior**:
  - Submits task data to API
  - Shows loading state during submission
  - Clears form after successful submission
- **Acceptance**: User can create tasks with valid data, errors shown for invalid inputs

### Task Edit Form
- **Fields**:
  - Title (required, max 255 characters)
  - Description (optional, text area)
  - Completed status (checkbox)
- **Validation**:
  - Title required validation
  - Title length validation
- **Behavior**:
  - Pre-populates with existing task data
  - Updates task via API
  - Shows loading state during submission
  - Closes form after successful update
- **Acceptance**: User can update existing tasks, changes saved correctly

## Validation Rules

### Input Validation
- **VR-001**: Email fields MUST follow standard email format validation
- **VR-002**: Password fields MUST require minimum 8 characters on signup
- **VR-003**: Task title fields MUST be required and have maximum 255 character limit
- **VR-004**: All required fields MUST show error state when empty on submission
- **VR-005**: Validation errors MUST be displayed near the relevant input field

### Form Submission Validation
- **VR-006**: Forms MUST validate required fields before API submission
- **VR-007**: Forms MUST show loading state during API requests
- **VR-008**: Forms MUST display server-side validation errors from API responses
- **VR-009**: Forms MUST prevent multiple rapid submissions during loading state
- **VR-010**: Forms MUST reset to initial state after successful submission

### Error Handling
- **VR-011**: All API error responses MUST be displayed in user-friendly format
- **VR-012**: Authentication errors MUST redirect to login page
- **VR-013**: Network errors MUST show appropriate messaging to user
- **VR-014**: Validation errors from API MUST highlight relevant form fields
- **VR-015**: Server errors MUST not expose internal details to user

## Auth-Aware Components

### ProtectedRoute Component
- **Purpose**: Wrapper component that restricts access to authenticated users
- **Props**:
  - `children`: Component(s) to render if user is authenticated
  - `redirectPath`: Path to redirect to if user is not authenticated (default: "/login")
- **Features**:
  - Checks authentication status
  - Redirects unauthenticated users to login
  - Renders children only for authenticated users
  - Preserves intended destination for post-login redirect
- **Acceptance**: Unauthenticated users are redirected to login, authenticated users see content

### AuthStatus Component
- **Purpose**: Component that displays authentication status and user controls
- **Props**:
  - `onLogout`: Function to handle logout action
- **Features**:
  - Shows user email when authenticated
  - Shows login/signup links when not authenticated
  - Shows logout button when authenticated
  - Updates display based on authentication status changes
- **Acceptance**: Correctly displays authentication state and appropriate controls

### LoadingSpinner Component
- **Purpose**: Visual indicator for loading states during API requests
- **Props**:
  - `show`: Boolean to control visibility
  - `message`: Optional string to display loading message
- **Features**:
  - Shows visual spinner animation
  - Optionally displays descriptive message
  - Can be overlay or inline depending on context
- **Acceptance**: Provides clear visual feedback during operations

### ErrorMessage Component
- **Purpose**: Consistent display of error messages throughout the application
- **Props**:
  - `message`: String with error message to display
  - `type`: String indicating error type ("error", "warning", "info") - default: "error"
  - `onDismiss`: Optional function to handle error dismissal
- **Features**:
  - Displays error message with appropriate styling
  - Color coding based on error type
  - Optional dismiss button
  - Accessible error announcements
- **Acceptance**: Error messages are displayed clearly and consistently

### SuccessMessage Component
- **Purpose**: Consistent display of success messages throughout the application
- **Props**:
  - `message`: String with success message to display
  - `autoDismiss`: Number of milliseconds before auto-dismissal (optional)
  - `onDismiss`: Optional function to handle message dismissal
- **Features**:
  - Displays success message with appropriate styling
  - Auto-dismiss capability
  - Optional dismiss button
- **Acceptance**: Success messages are displayed clearly and consistently