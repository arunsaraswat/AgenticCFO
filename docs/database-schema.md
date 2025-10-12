# Database Schema Documentation

## Overview

AgenticCFO uses PostgreSQL via Supabase with SQLAlchemy ORM and Alembic for migrations.

## Schema Version

Current schema version: **001** (Initial Migration)

## Tables

### Users Table

The `users` table stores all user account information and authentication data.

#### Table Definition

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_email ON users (email);
```

#### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique identifier for each user |
| `email` | VARCHAR | UNIQUE, NOT NULL, INDEXED | User's email address (login identifier) |
| `full_name` | VARCHAR | NOT NULL | User's full name for display |
| `hashed_password` | VARCHAR | NOT NULL | bcrypt hashed password |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether the account is active |
| `is_superuser` | BOOLEAN | NOT NULL, DEFAULT FALSE | Admin privileges flag |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp (auto-updated) |

#### Indexes

- **Primary Key**: `id` (automatic B-tree index)
- **Unique Index**: `email` (ensures email uniqueness, improves login query performance)

#### Constraints

- `email` must be unique across all users
- `email` must be a valid email format (validated at application level)
- `hashed_password` must be bcrypt hash (validated at application level)
- All NOT NULL fields must have values

## SQLAlchemy Model

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow, nullable=False)
```

## Data Types

### Password Hashing

Passwords are hashed using **bcrypt** with automatic salt generation:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash(plain_password)
```

Example hashed password:
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJlY6P9pO
```

### Timestamps

All timestamps are stored in UTC using PostgreSQL's `TIMESTAMP` type:
- `created_at`: Set once on user creation
- `updated_at`: Automatically updated on any model modification

## Sample Data

### Example User Record

```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJlY6P9pO",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
```

### Seed Data

The seed script (`backend/scripts/seed.py`) creates the following test users:

1. **Admin User**
   - Email: `admin@agenticcfo.com`
   - Password: `admin123456`
   - is_superuser: `true`

2. **Regular Users**
   - `john.doe@example.com` (password: `johndoe123`)
   - `jane.smith@example.com` (password: `janesmith123`)
   - `bob.wilson@example.com` (password: `bobwilson123`)

## Database Queries

### Common Queries

#### Find User by Email
```python
user = db.query(User).filter(User.email == "user@example.com").first()
```

Equivalent SQL:
```sql
SELECT * FROM users WHERE email = 'user@example.com' LIMIT 1;
```

#### Find User by ID
```python
user = db.query(User).filter(User.id == 1).first()
```

Equivalent SQL:
```sql
SELECT * FROM users WHERE id = 1 LIMIT 1;
```

#### Get All Active Users
```python
users = db.query(User).filter(User.is_active == True).all()
```

Equivalent SQL:
```sql
SELECT * FROM users WHERE is_active = TRUE;
```

#### Count Total Users
```python
count = db.query(User).count()
```

Equivalent SQL:
```sql
SELECT COUNT(*) FROM users;
```

## Migrations

### Current Migrations

#### Migration 001: Initial Migration
- **File**: `alembic/versions/20250112_0100-001_initial_migration.py`
- **Created**: 2025-01-12
- **Description**: Creates initial users table with all fields and indexes

#### Migration Commands

```bash
# View current migration version
alembic current

# View migration history
alembic history

# Upgrade to latest version
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Create new migration
alembic revision --autogenerate -m "description"
```

### Creating New Migrations

1. **Modify SQLAlchemy models** in `backend/app/models/`
2. **Generate migration**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "add new column"
   ```
3. **Review generated migration** in `alembic/versions/`
4. **Apply migration**:
   ```bash
   alembic upgrade head
   ```

## Data Validation

### Application Level Validation

#### Registration
- Email: Must be valid email format
- Password: Minimum 8 characters
- Full Name: Minimum 2 characters

#### Login
- Email: Must be valid email format
- Password: Minimum 8 characters

### Database Level Validation

- Email uniqueness (UNIQUE constraint)
- NOT NULL constraints on all required fields
- Boolean type validation for is_active and is_superuser

## Security Considerations

### Password Storage
- ✅ Never store plain text passwords
- ✅ Use bcrypt with automatic salt
- ✅ Bcrypt cost factor: 12 (configurable)

### Email Security
- ✅ Email uniqueness enforced at database level
- ✅ Case-insensitive email comparison (handle at app level)
- ✅ Email validation with regex at application level

### Data Access
- ✅ Use parameterized queries (SQLAlchemy ORM)
- ✅ Prevent SQL injection
- ✅ Row-level security with JWT user context

## Performance Optimization

### Indexes

Current indexes optimize:
1. **Login queries**: Email lookup O(log n) with B-tree index
2. **User lookup by ID**: Primary key index (automatic)

### Query Optimization

```python
# Good: Use indexed email column
user = db.query(User).filter(User.email == email).first()

# Bad: Full table scan on unindexed column
user = db.query(User).filter(User.full_name == name).first()
```

### Recommended Additional Indexes

For future scaling:
```sql
-- If filtering by is_active becomes common
CREATE INDEX ix_users_is_active ON users (is_active);

-- If filtering by created_at becomes common
CREATE INDEX ix_users_created_at ON users (created_at DESC);
```

## Backup and Recovery

### Supabase Automatic Backups

Supabase provides automatic daily backups. To restore:
1. Go to Supabase Dashboard
2. Navigate to Database > Backups
3. Select backup and restore

### Manual Backup

```bash
# Export database
pg_dump -h db.[PROJECT-REF].supabase.co -U postgres -d postgres > backup.sql

# Import database
psql -h db.[PROJECT-REF].supabase.co -U postgres -d postgres < backup.sql
```

## Future Schema Enhancements

### Potential Additions

1. **Password Reset Tokens**
```sql
CREATE TABLE password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token VARCHAR UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

2. **User Sessions**
```sql
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token_hash VARCHAR NOT NULL,
    ip_address VARCHAR,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3. **Audit Log**
```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR NOT NULL,
    resource VARCHAR,
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. **User Preferences**
```sql
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    theme VARCHAR DEFAULT 'light',
    language VARCHAR DEFAULT 'en',
    notifications BOOLEAN DEFAULT TRUE,
    preferences JSONB,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### Common Issues

#### "Email already registered" error
- Check if user exists: `SELECT * FROM users WHERE email = 'email@example.com';`
- If ghost record, delete: `DELETE FROM users WHERE email = 'email@example.com';`

#### Migration conflicts
- Check current version: `alembic current`
- View history: `alembic history`
- If needed, manually sync: `alembic stamp head`

#### Connection errors
- Verify DATABASE_URL in `.env`
- Check Supabase project status
- Ensure IP is whitelisted in Supabase settings

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)
