/**
 * Authentication service for user operations.
 */
import apiClient from './api';
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  UserProfile,
  DashboardData,
} from '@/types';
import { setToken, removeToken } from '@/utils/tokenManager';

/**
 * Authentication service class with static methods.
 */
class AuthService {
  /**
   * Login user with email and password.
   * @param credentials - User login credentials
   * @returns Login response with JWT token
   */
  static async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>('/api/auth/login', credentials);
    setToken(response.data.access_token);
    return response.data;
  }

  /**
   * Register a new user.
   * @param userData - User registration data
   * @returns Registration response
   */
  static async register(userData: RegisterRequest): Promise<RegisterResponse> {
    const response = await apiClient.post<RegisterResponse>('/api/auth/register', userData);
    return response.data;
  }

  /**
   * Logout current user by removing token.
   */
  static logout(): void {
    removeToken();
  }

  /**
   * Get current user's profile.
   * @returns User profile data
   */
  static async getProfile(): Promise<UserProfile> {
    const response = await apiClient.get<UserProfile>('/api/users/profile');
    return response.data;
  }

  /**
   * Get dashboard data for current user.
   * @returns Dashboard data
   */
  static async getDashboardData(): Promise<DashboardData> {
    const response = await apiClient.get<DashboardData>('/api/dashboard');
    return response.data;
  }
}

export default AuthService;
