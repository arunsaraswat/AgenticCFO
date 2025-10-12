/**
 * Custom hook for accessing authentication context.
 */
import { useContext } from 'react';
import { AuthContext } from '@/context/AuthContext';
import { AuthContextValue } from '@/types';

/**
 * Hook to access authentication context.
 * Must be used within an AuthProvider.
 * @returns Authentication context value
 * @throws Error if used outside AuthProvider
 */
export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
};
