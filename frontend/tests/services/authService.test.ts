/**
 * Tests for authentication service.
 */
import AuthService from '@/services/authService';
import apiClient from '@/services/api';
import { setToken, removeToken } from '@/utils/tokenManager';

// Mock axios and token manager
jest.mock('@/services/api');
jest.mock('@/utils/tokenManager');

const mockedApiClient = apiClient as jest.Mocked<typeof apiClient>;
const mockedSetToken = setToken as jest.MockedFunction<typeof setToken>;
const mockedRemoveToken = removeToken as jest.MockedFunction<typeof removeToken>;

describe('AuthService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('login', () => {
    it('successfully logs in and stores token', async () => {
      const mockResponse = {
        data: {
          access_token: 'test_token',
          token_type: 'bearer',
        },
      };

      mockedApiClient.post.mockResolvedValueOnce(mockResponse);

      const result = await AuthService.login({
        email: 'test@example.com',
        password: 'password123',
      });

      expect(mockedApiClient.post).toHaveBeenCalledWith('/api/auth/login', {
        email: 'test@example.com',
        password: 'password123',
      });
      expect(mockedSetToken).toHaveBeenCalledWith('test_token');
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('register', () => {
    it('successfully registers a user', async () => {
      const mockResponse = {
        data: {
          id: 1,
          email: 'test@example.com',
          full_name: 'Test User',
          message: 'User registered successfully',
        },
      };

      mockedApiClient.post.mockResolvedValueOnce(mockResponse);

      const result = await AuthService.register({
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User',
      });

      expect(mockedApiClient.post).toHaveBeenCalledWith('/api/auth/register', {
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User',
      });
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('logout', () => {
    it('removes token from storage', () => {
      AuthService.logout();
      expect(mockedRemoveToken).toHaveBeenCalled();
    });
  });

  describe('getProfile', () => {
    it('fetches user profile', async () => {
      const mockProfile = {
        data: {
          id: 1,
          email: 'test@example.com',
          full_name: 'Test User',
          is_active: true,
          created_at: '2024-01-01T00:00:00',
          updated_at: '2024-01-01T00:00:00',
          is_superuser: false,
        },
      };

      mockedApiClient.get.mockResolvedValueOnce(mockProfile);

      const result = await AuthService.getProfile();

      expect(mockedApiClient.get).toHaveBeenCalledWith('/api/users/profile');
      expect(result).toEqual(mockProfile.data);
    });
  });

  describe('getDashboardData', () => {
    it('fetches dashboard data', async () => {
      const mockDashboard = {
        data: {
          user: {
            id: 1,
            email: 'test@example.com',
            full_name: 'Test User',
            is_active: true,
            created_at: '2024-01-01T00:00:00',
          },
          stats: { total_items: 42 },
          message: 'Welcome back!',
        },
      };

      mockedApiClient.get.mockResolvedValueOnce(mockDashboard);

      const result = await AuthService.getDashboardData();

      expect(mockedApiClient.get).toHaveBeenCalledWith('/api/dashboard');
      expect(result).toEqual(mockDashboard.data);
    });
  });
});
