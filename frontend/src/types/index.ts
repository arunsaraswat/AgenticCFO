/**
 * TypeScript type definitions for the application.
 */

/**
 * User interface representing a user in the system.
 */
export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

/**
 * Extended user profile with additional information.
 */
export interface UserProfile extends User {
  updated_at: string;
  is_superuser: boolean;
}

/**
 * Login request payload.
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Login response with JWT token.
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

/**
 * Registration request payload.
 */
export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

/**
 * Registration response.
 */
export interface RegisterResponse {
  id: number;
  email: string;
  full_name: string;
  message: string;
}

/**
 * Dashboard data interface.
 */
export interface DashboardData {
  user: User;
  stats: Record<string, number>;
  message: string;
}

/**
 * API error response structure.
 */
export interface ApiError {
  detail: string;
}

/**
 * Authentication context value.
 */
export interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}
