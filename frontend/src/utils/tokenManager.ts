/**
 * Token management utilities for JWT authentication.
 */

const TOKEN_KEY = 'auth_token';

/**
 * Store JWT token in localStorage.
 * @param token - JWT token to store
 */
export const setToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Retrieve JWT token from localStorage.
 * @returns JWT token or null if not found
 */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Remove JWT token from localStorage.
 */
export const removeToken = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

/**
 * Check if user has a valid token.
 * Note: This only checks if token exists, not if it's valid/expired.
 * @returns True if token exists, false otherwise
 */
export const hasToken = (): boolean => {
  return getToken() !== null;
};
