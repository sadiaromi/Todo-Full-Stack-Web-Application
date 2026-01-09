// Constants for the Todo App

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    SIGNUP: `${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`,
    LOGIN: `${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`,
    LOGOUT: `${process.env.NEXT_PUBLIC_API_URL}/api/auth/logout`,
    REFRESH: `${process.env.NEXT_PUBLIC_API_URL}/api/auth/refresh`,
  },
  TASKS: {
    BASE: `${process.env.NEXT_PUBLIC_API_URL}/api/tasks`,
    GET_ALL: `${process.env.NEXT_PUBLIC_API_URL}/api/tasks`,
    CREATE: `${process.env.NEXT_PUBLIC_API_URL}/api/tasks`,
    UPDATE: (id) => `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}`,
    DELETE: (id) => `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}`,
    GET_BY_ID: (id) => `${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}`,
  },
  HEALTH: `${process.env.NEXT_PUBLIC_API_URL}/api/health`,
};

// Error messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred',
  UNAUTHORIZED: 'Unauthorized access',
  FORBIDDEN: 'Access forbidden',
  RATE_LIMITED: 'Rate limit exceeded',
  INVALID_TASK_TITLE: 'Task title must be 100 characters or less',
  INVALID_TASK_DESCRIPTION: 'Task description must be 1000 characters or less',
};

// Validation constants
export const VALIDATION = {
  MAX_TITLE_LENGTH: 100,
  MAX_DESCRIPTION_LENGTH: 1000,
  MIN_PASSWORD_LENGTH: 8,
};

// Status constants
export const TASK_STATUS = {
  ALL: 'all',
  COMPLETED: 'completed',
  INCOMPLETE: 'incomplete',
};

// Storage keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
};

// API configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  TIMEOUT: 10000, // 10 seconds
};