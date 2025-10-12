# API Usage Examples

Complete examples for all API endpoints with request/response samples.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer {access_token}
```

## API Endpoints

### 1. User Registration

Register a new user account.

#### Request

```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securepass123",
  "full_name": "John Doe"
}
```

#### Response (201 Created)

```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "message": "User registered successfully"
}
```

#### Error Responses

**400 Bad Request** - Email already registered
```json
{
  "detail": "Email already registered"
}
```

**422 Unprocessable Entity** - Validation error
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

#### cURL Example

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securepass123",
    "full_name": "John Doe"
  }'
```

#### JavaScript Example

```javascript
const response = await fetch('http://localhost:8000/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john.doe@example.com',
    password: 'securepass123',
    full_name: 'John Doe',
  }),
});

const data = await response.json();
console.log(data);
```

#### Python Example

```python
import requests

response = requests.post(
    'http://localhost:8000/api/auth/register',
    json={
        'email': 'john.doe@example.com',
        'password': 'securepass123',
        'full_name': 'John Doe'
    }
)

data = response.json()
print(data)
```

---

### 2. User Login

Authenticate and receive JWT token.

#### Request

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securepass123"
}
```

#### Response (200 OK)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTcwNTM0MjgwMH0.Xj8kN7L9mP4qR5sT6uV8wX0yZ1aB2cD3eF4gH5iJ6k",
  "token_type": "bearer"
}
```

#### Error Responses

**401 Unauthorized** - Invalid credentials
```json
{
  "detail": "Incorrect email or password"
}
```

**400 Bad Request** - Inactive user
```json
{
  "detail": "Inactive user account"
}
```

#### cURL Example

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "securepass123"
  }'
```

#### JavaScript Example

```javascript
const response = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john.doe@example.com',
    password: 'securepass123',
  }),
});

const data = await response.json();
localStorage.setItem('auth_token', data.access_token);
```

#### Python Example

```python
import requests

response = requests.post(
    'http://localhost:8000/api/auth/login',
    json={
        'email': 'john.doe@example.com',
        'password': 'securepass123'
    }
)

data = response.json()
token = data['access_token']
```

---

### 3. Get User Profile

Retrieve current user's profile information.

**🔒 Protected Endpoint** - Requires authentication

#### Request

```http
GET /api/users/profile
Authorization: Bearer {access_token}
```

#### Response (200 OK)

```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z",
  "is_superuser": false
}
```

#### Error Responses

**401 Unauthorized** - Missing or invalid token
```json
{
  "detail": "Could not validate credentials"
}
```

#### cURL Example

```bash
curl -X GET http://localhost:8000/api/users/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### JavaScript Example

```javascript
const token = localStorage.getItem('auth_token');

const response = await fetch('http://localhost:8000/api/users/profile', {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});

const profile = await response.json();
console.log(profile);
```

#### Python Example

```python
import requests

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(
    'http://localhost:8000/api/users/profile',
    headers=headers
)

profile = response.json()
print(profile)
```

---

### 4. Get Dashboard Data

Retrieve dashboard data with statistics.

**🔒 Protected Endpoint** - Requires authentication

#### Request

```http
GET /api/dashboard
Authorization: Bearer {access_token}
```

#### Response (200 OK)

```json
{
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00.000Z"
  },
  "stats": {
    "total_items": 42,
    "active_projects": 5,
    "completed_tasks": 28,
    "pending_tasks": 14
  },
  "message": "Welcome back, John Doe!"
}
```

#### Error Responses

**401 Unauthorized** - Missing or invalid token
```json
{
  "detail": "Could not validate credentials"
}
```

#### cURL Example

```bash
curl -X GET http://localhost:8000/api/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### JavaScript Example

```javascript
const token = localStorage.getItem('auth_token');

const response = await fetch('http://localhost:8000/api/dashboard', {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});

const dashboard = await response.json();
console.log(dashboard);
```

#### Python Example

```python
import requests

headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(
    'http://localhost:8000/api/dashboard',
    headers=headers
)

dashboard = response.json()
print(dashboard)
```

---

### 5. Health Check

Check if the API is running.

#### Request

```http
GET /health
```

#### Response (200 OK)

```json
{
  "status": "healthy",
  "app_name": "AgenticCFO"
}
```

#### cURL Example

```bash
curl -X GET http://localhost:8000/health
```

---

## Complete Workflow Examples

### User Registration and Login Flow

```javascript
// 1. Register new user
async function registerUser() {
  const response = await fetch('http://localhost:8000/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'john.doe@example.com',
      password: 'securepass123',
      full_name: 'John Doe',
    }),
  });

  const data = await response.json();
  console.log('Registered:', data);
}

// 2. Login
async function login() {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'john.doe@example.com',
      password: 'securepass123',
    }),
  });

  const data = await response.json();
  localStorage.setItem('auth_token', data.access_token);
  return data.access_token;
}

// 3. Get profile
async function getProfile(token) {
  const response = await fetch('http://localhost:8000/api/users/profile', {
    headers: { 'Authorization': `Bearer ${token}` },
  });

  const profile = await response.json();
  console.log('Profile:', profile);
  return profile;
}

// 4. Get dashboard
async function getDashboard(token) {
  const response = await fetch('http://localhost:8000/api/dashboard', {
    headers: { 'Authorization': `Bearer ${token}` },
  });

  const dashboard = await response.json();
  console.log('Dashboard:', dashboard);
  return dashboard;
}

// Execute workflow
async function completeWorkflow() {
  await registerUser();
  const token = await login();
  await getProfile(token);
  await getDashboard(token);
}
```

### Python Complete Workflow

```python
import requests

BASE_URL = 'http://localhost:8000'

class AgenticCFOClient:
    def __init__(self):
        self.token = None

    def register(self, email, password, full_name):
        """Register a new user."""
        response = requests.post(
            f'{BASE_URL}/api/auth/register',
            json={
                'email': email,
                'password': password,
                'full_name': full_name
            }
        )
        return response.json()

    def login(self, email, password):
        """Login and store token."""
        response = requests.post(
            f'{BASE_URL}/api/auth/login',
            json={'email': email, 'password': password}
        )
        data = response.json()
        self.token = data['access_token']
        return data

    def get_profile(self):
        """Get user profile."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f'{BASE_URL}/api/users/profile',
            headers=headers
        )
        return response.json()

    def get_dashboard(self):
        """Get dashboard data."""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f'{BASE_URL}/api/dashboard',
            headers=headers
        )
        return response.json()

# Usage
client = AgenticCFOClient()

# Register
client.register('john@example.com', 'password123', 'John Doe')

# Login
client.login('john@example.com', 'password123')

# Get profile
profile = client.get_profile()
print(f"User: {profile['full_name']}")

# Get dashboard
dashboard = client.get_dashboard()
print(f"Message: {dashboard['message']}")
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Specific error message"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 422 Unprocessable Entity (Validation Error)
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

### Error Handling Example

```javascript
async function apiCall() {
  try {
    const response = await fetch('http://localhost:8000/api/users/profile', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid - redirect to login
        window.location.href = '/login';
      } else if (response.status === 422) {
        // Validation error
        const error = await response.json();
        console.error('Validation errors:', error.detail);
      } else {
        // Other error
        const error = await response.json();
        console.error('Error:', error.detail);
      }
      return;
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:

- Rate limiting middleware
- Per-user request limits
- API key based throttling

## API Versioning

Current API version: **v1** (implied in all routes)

Future versions would use: `/api/v2/auth/login`

## Interactive API Documentation

Visit these URLs when the backend is running:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing
  - Request/response examples
  - Schema exploration

- **ReDoc**: http://localhost:8000/redoc
  - Alternative documentation UI
  - Clean, readable format
  - Downloadable OpenAPI spec

## Postman Collection

Import this JSON to create a Postman collection:

```json
{
  "info": {
    "name": "AgenticCFO API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Register",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\",\n  \"full_name\": \"Test User\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/auth/register",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "auth", "register"]
        }
      }
    }
  ]
}
```
