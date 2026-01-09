// Frontend API client for the Todo App
import axios from 'axios';
import AuthService from './auth';
import { API_CONFIG, API_ENDPOINTS, ERROR_MESSAGES, TASK_STATUS } from './constants';
import { taskCache } from './cache';
import { debounce } from './performance';

class ApiClient {
  constructor() {
    this.auth = AuthService;
    this.api = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Set up interceptors to handle authentication
    this.setupInterceptors();
  }

  setupInterceptors() {
    // Request interceptor to add token to headers
    this.api.interceptors.request.use(
      (config) => {
        const token = this.auth.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        console.error(ERROR_MESSAGES.NETWORK_ERROR, error);
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle errors
    this.api.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        // Handle specific error cases
        if (error.response?.status === 401) {
          // Unauthorized - likely token expired
          this.auth.logout();
        } else if (error.response?.status === 403) {
          // Forbidden - user doesn't have permission
          console.error(ERROR_MESSAGES.FORBIDDEN, error.response.data);
        } else if (error.response?.status === 429) {
          // Rate limited
          console.error(ERROR_MESSAGES.RATE_LIMITED, error.response.data);
        } else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
          console.error('Request timed out');
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication endpoints
  async signup(email, password) {
    return this.auth.signup(email, password);
  }

  async login(email, password) {
    return this.auth.login(email, password);
  }

  async logout() {
    this.auth.logout();
  }

  // Task endpoints with caching
  async getTasks(status = null) {
    // Create cache key based on status
    const cacheKey = `tasks_${status || 'all'}`;

    // Try to get from cache first
    const cachedData = taskCache.get(cacheKey);
    if (cachedData) {
      return cachedData;
    }

    let url = API_ENDPOINTS.TASKS.GET_ALL;
    if (status && [TASK_STATUS.ALL, TASK_STATUS.COMPLETED, TASK_STATUS.IN_COMPLETE].includes(status)) {
      url += `?status=${status}`;
    }

    const response = await this.api.get(url);
    const data = response.data;

    // Cache the response for 2 minutes
    taskCache.set(cacheKey, data, 2 * 60 * 1000);

    return data;
  }

  async createTask(title, description = null, completed = false) {
    const response = await this.api.post(API_ENDPOINTS.TASKS.CREATE, {
      title,
      description,
      completed
    });

    const data = response.data;

    // Invalidate related cache entries
    taskCache.delete('tasks_all');
    taskCache.delete('tasks_completed');
    taskCache.delete('tasks_incomplete');

    return data;
  }

  async updateTask(taskId, title = null, description = null, completed = null) {
    const response = await this.api.put(API_ENDPOINTS.TASKS.UPDATE(taskId), {
      title,
      description,
      completed
    });

    const data = response.data;

    // Invalidate related cache entries
    taskCache.delete('tasks_all');
    taskCache.delete('tasks_completed');
    taskCache.delete('tasks_incomplete');
    taskCache.delete(`task_${taskId}`);

    return data;
  }

  async deleteTask(taskId) {
    const response = await this.api.delete(API_ENDPOINTS.TASKS.DELETE(taskId));

    // Invalidate related cache entries
    taskCache.delete('tasks_all');
    taskCache.delete('tasks_completed');
    taskCache.delete('tasks_incomplete');
    taskCache.delete(`task_${taskId}`);

    return response.data;
  }

  async getTask(taskId) {
    // Create cache key for specific task
    const cacheKey = `task_${taskId}`;

    // Try to get from cache first
    const cachedData = taskCache.get(cacheKey);
    if (cachedData) {
      return cachedData;
    }

    const response = await this.api.get(API_ENDPOINTS.TASKS.GET_BY_ID(taskId));
    const data = response.data;

    // Cache the response for 2 minutes
    taskCache.set(cacheKey, data, 2 * 60 * 1000);

    return data;
  }

  // Debounced version of getTasks for search/filtering
  debouncedGetTasks = debounce(async (status = null) => {
    return this.getTasks(status);
  }, 300);

  // Clear task cache
  clearTaskCache() {
    taskCache.clear();
  }
}

export default new ApiClient();