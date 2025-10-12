# Quick Setup Guide

Get AgenticCFO running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (requires 3.9+)
python3 --version

# Check Node.js version (requires 18+)
node --version

# Check npm
npm --version
```

## Step 1: Get Supabase Credentials

1. Go to [Supabase](https://supabase.com)
2. Create a new project (or use existing)
3. Go to Project Settings > Database
4. Copy your connection string

Example format:
```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

## Step 2: Configure Backend

```bash
cd backend

# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or use your favorite editor
```

**Required changes in .env:**
```env
# Replace with your Supabase connection string
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres

# Generate a secure secret key (or keep the default for development)
SECRET_KEY=your-secret-key-change-in-production
```

## Step 3: Configure Frontend (Optional)

```bash
cd frontend
cp .env.example .env
```

The defaults should work for local development. Only change if needed.

## Step 4: Install Backend Dependencies

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 5: Setup Database

```bash
# Still in backend directory with venv activated

# Run migrations to create tables
./migrate.sh upgrade

# (Optional) Seed with test data
./seed.sh
```

## Step 6: Install Frontend Dependencies

```bash
cd frontend

# Install npm packages
npm install
```

## Step 7: Run the Application

### Option A: Run Everything at Once (Recommended)

```bash
# From project root
./run.sh
```

This will:
- Check all dependencies
- Run migrations
- Start backend (port 8000)
- Start frontend (port 5173)

### Option B: Run Separately

Terminal 1 (Backend):
```bash
cd backend
./start.sh
```

Terminal 2 (Frontend):
```bash
cd frontend
./start.sh
```

## Step 8: Access the Application

Open your browser:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Test It Out

### With Seed Data

If you ran `./seed.sh`, you can login with:
- Email: `admin@agenticcfo.com`
- Password: `admin123456`

Or any of the test users (see backend/scripts/seed.py for credentials)

### Create New Account

1. Go to http://localhost:5173
2. Click "Get Started" or "create a new account"
3. Fill in the registration form
4. You'll be automatically logged in

## Running Tests

### Backend Tests
```bash
cd backend
./test.sh
```

### Frontend Tests
```bash
cd frontend
./test.sh
```

## Common Issues

### "Database connection failed"
- Check your DATABASE_URL in backend/.env
- Verify Supabase project is active
- Ensure your IP is whitelisted in Supabase

### "Module not found" errors
Backend:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port already in use
```bash
# Find and kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

### Migration errors
```bash
cd backend
./migrate.sh history  # Check migration status
./migrate.sh upgrade  # Try running again
```

## Next Steps

Once everything is running:

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read the docs**: Check the `docs/` folder
3. **Run tests**: Ensure everything works
4. **Start building**: Add your own features!

## Development Workflow

```bash
# Start development
./run.sh

# Make changes to code (auto-reloads on save)

# Test backend changes
cd backend && ./test.sh

# Test frontend changes
cd frontend && npm run test:watch

# Create new migration after model changes
cd backend && ./migrate.sh create "your migration message"
```

## Getting Help

- Check [README.md](README.md) for detailed documentation
- See [docs/architecture.md](docs/architecture.md) for architecture details
- See [docs/api-examples.md](docs/api-examples.md) for API usage
- Check [docs/database-schema.md](docs/database-schema.md) for database info

## Success Indicators

You know everything is working when:

✅ Backend starts without errors on port 8000
✅ Frontend starts without errors on port 5173
✅ You can visit http://localhost:8000/docs and see API documentation
✅ You can visit http://localhost:5173 and see the login page
✅ You can register a new account
✅ You can login and see the dashboard
✅ Backend tests pass with `./test.sh`
✅ Frontend tests pass with `./test.sh`

## Time Estimate

- **Supabase setup**: 5 minutes
- **Configuration**: 2 minutes
- **Dependencies installation**: 5-10 minutes
- **First run**: 2 minutes

**Total: ~15-20 minutes**

---

**Happy coding! 🚀**
