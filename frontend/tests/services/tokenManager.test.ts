/**
 * Tests for token manager utilities.
 */
import { setToken, getToken, removeToken, hasToken } from '@/utils/tokenManager';

describe('Token Manager', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  describe('setToken', () => {
    it('stores token in localStorage', () => {
      setToken('test_token');
      expect(localStorage.setItem).toHaveBeenCalledWith('auth_token', 'test_token');
    });
  });

  describe('getToken', () => {
    it('retrieves token from localStorage', () => {
      (localStorage.getItem as jest.Mock).mockReturnValue('test_token');
      const token = getToken();
      expect(localStorage.getItem).toHaveBeenCalledWith('auth_token');
      expect(token).toBe('test_token');
    });

    it('returns null when no token exists', () => {
      (localStorage.getItem as jest.Mock).mockReturnValue(null);
      const token = getToken();
      expect(token).toBeNull();
    });
  });

  describe('removeToken', () => {
    it('removes token from localStorage', () => {
      removeToken();
      expect(localStorage.removeItem).toHaveBeenCalledWith('auth_token');
    });
  });

  describe('hasToken', () => {
    it('returns true when token exists', () => {
      (localStorage.getItem as jest.Mock).mockReturnValue('test_token');
      expect(hasToken()).toBe(true);
    });

    it('returns false when no token exists', () => {
      (localStorage.getItem as jest.Mock).mockReturnValue(null);
      expect(hasToken()).toBe(false);
    });
  });
});
