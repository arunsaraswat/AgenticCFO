/**
 * Authentication context for managing global auth state.
 */
import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthContextValue } from '@/types';
import AuthService from '@/services/authService';
import { hasToken, removeToken } from '@/utils/tokenManager';

/**
 * Authentication context.
 */
export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Authentication provider component.
 * Manages authentication state and provides auth methods to children.
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Load user profile on mount if token exists.
   */
  useEffect(() => {
    const loadUser = async () => {
      if (hasToken()) {
        try {
          const profile = await AuthService.getProfile();
          setUser(profile);
        } catch (error) {
          console.error('Failed to load user profile:', error);
          removeToken();
        }
      }
      setIsLoading(false);
    };

    loadUser();
  }, []);

  /**
   * Login user with email and password.
   * @param email - User email
   * @param password - User password
   */
  const login = async (email: string, password: string): Promise<void> => {
    await AuthService.login({ email, password });
    const profile = await AuthService.getProfile();
    setUser(profile);
  };

  /**
   * Register a new user.
   * @param email - User email
   * @param password - User password
   * @param fullName - User's full name
   */
  const register = async (
    email: string,
    password: string,
    fullName: string
  ): Promise<void> => {
    await AuthService.register({ email, password, full_name: fullName });
    // Auto-login after registration
    await login(email, password);
  };

  /**
   * Logout current user.
   */
  const logout = (): void => {
    AuthService.logout();
    setUser(null);
  };

  const value: AuthContextValue = {
    user,
    isAuthenticated: user !== null,
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
