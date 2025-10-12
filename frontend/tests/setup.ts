/**
 * Jest test setup configuration.
 */
import '@testing-library/jest-dom';

// Mock environment variables
process.env.VITE_API_BASE_URL = 'http://localhost:8000';
process.env.VITE_APP_NAME = 'AgenticCFO';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

global.localStorage = localStorageMock as any;

// Mock window.location
delete (window as any).location;
window.location = {
  ...window.location,
  href: '',
  pathname: '/',
} as any;
