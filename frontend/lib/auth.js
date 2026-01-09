// Frontend authentication utilities for the Todo App
import axios from 'axios';
import { API_CONFIG, API_ENDPOINTS, STORAGE_KEYS } from './constants';

class AuthService {
  constructor() {
    this.apiBase = API_CONFIG.BASE_URL;
    this.token = null;
    this.isRefreshing = false;
    this.failedQueue = [];

    // Set up axios interceptor to include token in requests
    this.setupAxiosInterceptors();
  }

  setupAxiosInterceptors() {
    // Request interceptor to add token to headers
    axios.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle token expiration and refresh
    axios.interceptors.response.use(
      (response) => {
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          // Mark the request as retry to avoid infinite loops
          originalRequest._retry = true;

          // Try to refresh the token
          const refreshToken = this.getRefreshToken();

          if (refreshToken) {
            try {
              const newToken = await this.refreshAccessToken(refreshToken);
              if (newToken) {
                // Update the token in the original request
                originalRequest.headers.Authorization = `Bearer ${newToken}`;
                // Retry the original request
                return axios(originalRequest);
              }
            } catch (refreshError) {
              // If refresh fails, logout the user
              this.logout();
              return Promise.reject(refreshError);
            }
          } else {
            // No refresh token available, logout the user
            this.logout();
          }
        }

        return Promise.reject(error);
      }
    );
  }

  async signup(email, password) {
    try {
      const response = await axios.post(`${this.apiBase}${API_ENDPOINTS.AUTH.SIGNUP}`, {
        email,
        password,
      });

      const { user, token, refresh_token } = response.data;
      this.setToken(token);
      this.setRefreshToken(refresh_token);

      return { user, token, refresh_token };
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Signup failed');
    }
  }

  async login(email, password) {
    try {
      const response = await axios.post(`${this.apiBase}${API_ENDPOINTS.AUTH.LOGIN}`, {
        email,
        password,
      });

      const { user, token, refresh_token } = response.data;
      this.setToken(token);
      this.setRefreshToken(refresh_token);

      return { user, token, refresh_token };
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  }

  logout() {
    this.setToken(null);
    this.setRefreshToken(null);
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  }

  setToken(token) {
    this.token = token;
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, token);
      } else {
        localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
      }
    }
  }

  getToken() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    }
    return this.token;
  }

  setRefreshToken(token) {
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, token);
      } else {
        localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
      }
    }
  }

  getRefreshToken() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
    }
    return null;
  }

  isAuthenticated() {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    // Check if token is expired
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Date.now() / 1000;
      return payload.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  async refreshAccessToken(refreshToken) {
    try {
      const response = await axios.post(`${this.apiBase}${API_ENDPOINTS.AUTH.REFRESH}`, {
        refresh_token: refreshToken
      });

      const { token } = response.data;
      this.setToken(token);
      return token;
    } catch (error) {
      console.error('Token refresh failed:', error);
      throw error;
    }
  }
}

export default new AuthService();