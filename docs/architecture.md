# Architecture Documentation

## System Architecture

AgenticCFO follows a modern three-tier architecture with clear separation of concerns.

## Backend Architecture

### Layers

#### 1. API Layer (`app/api/`)
- **Responsibility**: HTTP request/response handling
- **Components**: FastAPI route handlers
- **Key Features**:
  - RESTful endpoint definitions
  - Request validation via Pydantic
  - Response serialization
  - Error handling

#### 2. Service Layer (`app/services/`)
- **Responsibility**: Business logic implementation
- **Components**: Service classes with static methods
- **Key Features**:
  - Authentication logic
  - User management
  - Data processing
  - Transactional operations

#### 3. Data Layer (`app/models/`, `app/db/`)
- **Responsibility**: Data persistence and retrieval
- **Components**: SQLAlchemy models, database session management
- **Key Features**:
  - ORM model definitions
  - Database session lifecycle
  - Migration support via Alembic

### Core Components

#### Configuration (`app/core/`)
```python
Settings (config.py)
    ├── Environment variables
    ├── Database configuration
    ├── JWT settings
    └── CORS origins

Security (security.py)
    ├── Password hashing (bcrypt)
    ├── JWT token creation/validation
    └── Authentication dependencies

Dependencies (dependencies.py)
    └── Dependency injection helpers
```

#### Authentication Flow
```
1. User submits credentials
   └─> POST /api/auth/login

2. AuthService validates credentials
   ├─> Check user exists
   ├─> Verify password (bcrypt)
   └─> Generate JWT token

3. Client stores token
   └─> localStorage.setItem('auth_token', token)

4. Subsequent requests include token
   └─> Authorization: Bearer {token}

5. Security middleware validates token
   ├─> decode_access_token()
   ├─> Fetch user from database
   └─> Inject user into route handler
```

## Frontend Architecture

### Component Hierarchy
```
App
├── AuthProvider (Context)
│   └── Router
│       ├── Public Routes
│       │   ├── Login Page
│       │   │   └── LoginForm
│       │   └── Register Page
│       │       └── RegisterForm
│       └── Protected Routes
│           ├── Dashboard Page
│           │   ├── Header
│           │   └── Stats Display
│           └── Profile Page
│               └── Header
```

### State Management

#### Authentication Context
```typescript
AuthContext
├── State
│   ├── user: User | null
│   ├── isAuthenticated: boolean
│   └── isLoading: boolean
├── Actions
│   ├── login(email, password)
│   ├── register(email, password, fullName)
│   └── logout()
└── Effects
    └── Load user on mount (if token exists)
```

#### Component Communication
```
Page Components
    └─> Use useAuth() hook
        └─> Access AuthContext
            ├─> Read user state
            └─> Call auth actions

Protected Routes
    └─> Check isAuthenticated
        ├─> True: Render children
        └─> False: Redirect to login
```

### Service Layer

#### API Service (`services/api.ts`)
- Axios instance with base configuration
- Request interceptor: Add JWT token
- Response interceptor: Handle 401 errors
- Automatic token refresh on expiry

#### Auth Service (`services/authService.ts`)
```typescript
AuthService
├── login(credentials)
├── register(userData)
├── logout()
├── getProfile()
└── getDashboardData()
```

### Routing Strategy
```
/ (root)
├── /login (public)
├── /register (public)
├── /dashboard (protected)
│   └── Requires: isAuthenticated = true
└── /profile (protected)
    └── Requires: isAuthenticated = true
```

## Data Flow

### Registration Flow
```
1. User fills RegisterForm
   └─> Client-side validation

2. Submit to backend
   └─> POST /api/auth/register

3. Backend processing
   ├─> Validate with Pydantic
   ├─> Check email uniqueness
   ├─> Hash password (bcrypt)
   └─> Insert into database

4. Auto-login after registration
   ├─> Call login()
   └─> Navigate to dashboard
```

### Authentication Flow
```
1. User fills LoginForm
   └─> Client-side validation

2. Submit to backend
   └─> POST /api/auth/login

3. Backend authentication
   ├─> Find user by email
   ├─> Verify password
   └─> Generate JWT token

4. Frontend token management
   ├─> Store in localStorage
   ├─> Fetch user profile
   ├─> Update AuthContext
   └─> Navigate to dashboard
```

### Protected API Request Flow
```
1. User navigates to Dashboard
   └─> Protected route check

2. Component requests data
   └─> AuthService.getDashboardData()

3. API client adds token
   └─> Axios interceptor adds Bearer token

4. Backend validates token
   ├─> JWT decode and verify
   ├─> Fetch user from database
   └─> Execute route handler

5. Response returned
   └─> Update component state
```

## Security Architecture

### Backend Security

#### Password Security
- Bcrypt hashing with salt
- Minimum length validation (8 characters)
- Never store plain text passwords

#### JWT Tokens
- HS256 algorithm
- Configurable expiration (default 30 minutes)
- Payload contains user identifier (email)
- Secret key from environment variable

#### API Protection
```python
@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_active_user)
):
    # Route only accessible with valid JWT token
    # current_user is automatically injected
    return {"user": current_user}
```

### Frontend Security

#### Token Management
- Stored in localStorage (consider httpOnly cookies for production)
- Automatically attached to requests
- Removed on logout or 401 error
- Not exposed in global scope

#### Protected Routes
```typescript
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>
```
- Check authentication before rendering
- Redirect to login if not authenticated
- Display loading spinner during auth check

#### Input Validation
- Client-side validation for UX
- Backend validation for security
- Both use similar rules (DRY principle)

## Database Architecture

### Schema Design

#### Users Table
```sql
users
├── id (Primary Key, Serial)
├── email (Unique, Indexed)
├── full_name
├── hashed_password
├── is_active (Boolean, Default: true)
├── is_superuser (Boolean, Default: false)
├── created_at (Timestamp)
└── updated_at (Timestamp, Auto-update)
```

### Migration Strategy

#### Alembic Configuration
```
alembic/
├── versions/
│   └── 001_initial_migration.py
├── env.py (Environment configuration)
└── script.py.mako (Template for new migrations)
```

#### Migration Commands
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View history
alembic history
```

## Testing Architecture

### Backend Testing Strategy

#### Test Layers
```
Unit Tests
├── Models (test_models.py)
│   └── Test database model behavior
├── Services (test_security.py)
│   └── Test business logic in isolation
└── Utilities
    └── Test helper functions

Integration Tests
├── API Endpoints (test_auth.py, test_users.py)
│   └── Test full request/response cycle
└── Database Operations
    └── Test with in-memory SQLite
```

#### Test Fixtures (conftest.py)
```python
@pytest.fixture
def db():
    # Fresh database for each test

@pytest.fixture
def client(db):
    # Test client with database override

@pytest.fixture
def test_user(db):
    # Pre-created test user

@pytest.fixture
def auth_headers(test_user_token):
    # Authentication headers
```

### Frontend Testing Strategy

#### Test Types
```
Unit Tests
├── Components (Button.test.tsx, Input.test.tsx)
│   └── Test component rendering and behavior
└── Services (authService.test.ts, tokenManager.test.ts)
    └── Test API calls and utilities

Integration Tests
└── User Flows
    └── Test complete user interactions
```

#### Test Setup
```typescript
// Mock API calls
jest.mock('@/services/api');

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
};
```

## Performance Considerations

### Backend Optimization
- Database connection pooling via SQLAlchemy
- Index on frequently queried fields (email)
- Async route handlers with FastAPI
- Response caching opportunities (Redis)

### Frontend Optimization
- Code splitting with React.lazy
- Vite for fast builds and HMR
- Tailwind CSS purging in production
- Axios interceptors reduce boilerplate

## Scalability

### Horizontal Scaling
- Stateless backend (JWT tokens)
- Database on managed service (Supabase)
- Frontend on CDN
- Load balancer for multiple backend instances

### Vertical Scaling
- Uvicorn workers for backend
- Database optimization (indexes, queries)
- Frontend bundle size optimization

## Deployment Architecture

### Development
```
Frontend (Vite Dev Server) :5173
    └─> Backend (Uvicorn) :8000
        └─> Supabase PostgreSQL
```

### Production
```
Frontend (CDN/Static Host)
    └─> Backend (Load Balanced)
        ├─> Instance 1
        ├─> Instance 2
        └─> Instance N
            └─> Supabase PostgreSQL (Managed)
```

## Future Enhancements

### Potential Additions
- Redis for caching and sessions
- WebSocket support for real-time features
- File upload handling
- Email verification
- Password reset flow
- Role-based access control (RBAC)
- Audit logging
- Rate limiting
- API versioning

### Infrastructure Improvements
- Docker containerization
- CI/CD pipeline (GitHub Actions)
- Monitoring and logging (Sentry, LogRocket)
- Performance monitoring (New Relic)
- Automated backups
- Blue-green deployment
