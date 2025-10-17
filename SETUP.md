# Agentic CFO Platform - Quick Setup Guide

Get the Agentic CFO Platform running in **under 20 minutes**!

---

## Prerequisites Check

Before starting, ensure you have:

```bash
# Check Python version (requires 3.11+)
python3 --version

# Check Node.js version (requires 18+)
node --version

# Check npm
npm --version

# Check Redis (or plan to use Redis Cloud)
redis-cli ping  # Should return PONG
```

You'll also need:
- **Supabase account** (free tier works): [supabase.com](https://supabase.com)
- **OpenRouter API key**: [openrouter.ai](https://openrouter.ai) (for LLM access)
- **Redis server** (local or cloud)

---

## Step 1: Get Supabase Database URL

1. Go to [Supabase](https://supabase.com) and log in
2. Create a new project (or use existing)
3. Go to **Project Settings** → **Database**
4. Copy your connection string (it looks like this):

```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

**💡 Tip:** Make sure to whitelist your IP address in Supabase settings → **Database** → **Connection pooling**

---

## Step 2: Get OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai) and sign up
2. Navigate to **Keys** in the dashboard
3. Create a new API key
4. Add some credits (minimum $5 recommended for testing)

**💡 Tip:** OpenRouter gives you access to GPT-4, Claude-3.5, and other models through a single API

---

## Step 3: Configure Backend

```bash
cd backend

# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use your favorite editor (vim, code, etc.)
```

**Update these required variables in `.env`:**

```env
# Database (from Step 1)
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres

# OpenRouter (from Step 2)
OPENROUTER_API_KEY=sk-or-v1-YOUR_API_KEY_HERE
OPENROUTER_DEFAULT_MODEL=openai/gpt-4-turbo

# Redis (use local or Redis Cloud URL)
REDIS_URL=redis://localhost:6379/0

# Security (generate a secure key)
SECRET_KEY=your-secret-key-change-in-production
# Generate with: openssl rand -hex 32

# ChromaDB (for mapping memory)
CHROMA_PERSIST_DIRECTORY=/tmp/agenticcfo/chroma

# File storage
ARTIFACTS_STORAGE_PATH=/tmp/agenticcfo/artifacts
MAX_UPLOAD_SIZE_MB=500

# CORS (for local development)
CORS_ORIGINS=http://localhost:5173
```

**Optional (but recommended for debugging):**

```env
# LangSmith (for debugging LangGraph workflows)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key  # Get from smith.langchain.com
LANGCHAIN_PROJECT=agenticcfo
```

---

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

**Expected time:** 5-10 minutes (depending on internet speed)

---

## Step 5: Setup Database

```bash
# Still in backend directory with venv activated

# Run migrations to create tables
./migrate.sh upgrade

# (Optional) Seed with test data
./seed.sh
```

**What this does:**
- Creates all database tables (users, tenants, file_uploads, datasets, work_orders, etc.)
- Sets up indexes and constraints
- (If seeding) Creates test users and sample data

**Expected time:** 1-2 minutes

---

## Step 6: Install Frontend Dependencies

```bash
cd ../frontend

# Install npm packages
npm install
```

**Expected time:** 3-5 minutes

**Optional:** Configure frontend environment (defaults work for local dev)

```bash
cp .env.example .env
# Edit if needed (default VITE_API_BASE_URL=http://localhost:8000 works)
```

---

## Step 7: Start Redis (if using local)

If you're using a local Redis server:

```bash
# Start Redis server
redis-server

# Or start as background service (macOS)
brew services start redis

# Or start as background service (Ubuntu/Debian)
sudo systemctl start redis
```

**💡 Tip:** If you're using **Redis Cloud**, skip this step and just use the cloud URL in your `.env`

---

## Step 8: Run the Application

### Option A: Run Everything at Once (Recommended)

From the project root:

```bash
./run.sh
```

**This will:**
- Check all dependencies
- Run database migrations
- Start backend (port 8000)
- Start Celery worker (for async agents)
- Start frontend (port 5173)

**Expected time:** 30 seconds

---

### Option B: Run Separately (for development)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
./start.sh
```

**Terminal 2 - Celery Worker (for async agent tasks):**
```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

**Terminal 3 - Frontend:**
```bash
cd frontend
./start.sh
```

---

## Step 9: Access the Application

Once all services are running:

- **Frontend (React App):** [http://localhost:5173](http://localhost:5173)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Docs (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Step 10: Test It Out

### With Seed Data

If you ran `./seed.sh`, you can login with:

**Admin User:**
- Email: `admin@agenticcfo.com`
- Password: `admin123456`

**Test Users:**
- See `backend/scripts/seed.py` for other test accounts

### Create New Account

1. Go to [http://localhost:5173](http://localhost:5173)
2. Click "Get Started" or "Create Account"
3. Fill in the registration form
4. You'll be automatically logged in

### Upload Your First File

1. Navigate to **Upload** page
2. Select a file (e.g., `TrialBalance.xlsx`)
3. Choose template type (or let auto-detection work)
4. Click "Upload"
5. Watch agents process your file in real-time via WebSocket updates!

---

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
./test.sh                 # Run all tests with coverage
./test.sh -v              # Verbose output
./test.sh -k test_agent   # Run specific test
```

**Coverage target:** 70%+

### Frontend Tests

```bash
cd frontend
./test.sh                 # Run all tests with coverage
npm run test:watch        # Watch mode for development
```

**Coverage target:** 70%+

---

## Common Issues & Solutions

### Issue: Database connection failed

**Solution:**
```bash
# Check your DATABASE_URL in backend/.env
# Verify Supabase project is active
# Ensure your IP is whitelisted in Supabase
```

### Issue: `ModuleNotFoundError` (Backend)

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Cannot connect to Redis

**Solution:**
```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Or start Redis
redis-server

# Or check REDIS_URL in .env
```

### Issue: OpenRouter API errors

**Solution:**
- Verify `OPENROUTER_API_KEY` in `.env`
- Check API credits at [openrouter.ai](https://openrouter.ai)
- Review model availability and rate limits

### Issue: Frontend build errors

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: Port already in use

**Solution:**
```bash
# Find and kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

### Issue: Migration errors

**Solution:**
```bash
cd backend
./migrate.sh history    # Check migration status
./migrate.sh downgrade  # Rollback if needed
./migrate.sh upgrade    # Try running again
```

---

## Next Steps

Once everything is running:

### 1. Explore the API
Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see interactive API documentation

### 2. Read the Architecture
Check [docs/architecture.md](docs/architecture.md) for comprehensive technical design (2,400+ lines!)

### 3. Run Tests
Ensure everything works by running the test suites

### 4. Upload Sample Files
Try uploading:
- **TrialBalance.xlsx** → triggers Close Copilot
- **BankStatement.csv** → triggers Cash Commander
- **AP_OpenItems.xlsx** → triggers Payables Protector
- **POS_Sales.csv** (Retail) → triggers GMROI Optimizer

### 5. Check Work Order Progress
Watch real-time agent execution via:
- Work Order dashboard (frontend)
- WebSocket console logs (browser DevTools)
- LangSmith traces (if configured)

---

## Development Workflow

```bash
# Start development environment
./run.sh

# Make code changes (auto-reloads on save)

# Run backend tests after changes
cd backend && ./test.sh

# Run frontend tests in watch mode
cd frontend && npm run test:watch

# Create new database migration (if models changed)
cd backend && ./migrate.sh create "your migration message"

# Apply new migration
./migrate.sh upgrade
```

---

## Environment Setup Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Supabase account created + database URL copied
- [ ] OpenRouter API key obtained + credits added
- [ ] Redis server running (local or cloud)
- [ ] Backend `.env` configured with all required variables
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Database migrations run (`./migrate.sh upgrade`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] All services started (`./run.sh` or manually)
- [ ] Application accessible at [http://localhost:5173](http://localhost:5173)
- [ ] API docs accessible at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Time Estimate

- **Supabase setup:** 5 minutes
- **OpenRouter setup:** 2 minutes
- **Backend configuration:** 3 minutes
- **Dependencies installation:** 8-15 minutes
- **Database migrations:** 2 minutes
- **First run:** 1 minute

**Total: ~20-30 minutes** (first time setup)

Subsequent starts: **~30 seconds** (just run `./run.sh`)

---

## Getting Help

If you encounter issues:

1. **Check the logs:**
   - Backend: Terminal running `./start.sh`
   - Celery: Terminal running Celery worker
   - Frontend: Terminal running `npm run dev`
   - Browser console: DevTools → Console

2. **Review documentation:**
   - [README.md](README.md) - Project overview
   - [docs/architecture.md](docs/architecture.md) - Technical design
   - [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - High-level summary

3. **Open an issue:**
   - GitHub Issues: [github.com/yourrepo/AgenticCFO/issues](https://github.com/yourrepo/AgenticCFO/issues)

4. **Email support:**
   - support@agenticcfo.com

---

## Success Indicators

You know everything is working when:

✅ Backend starts without errors on port 8000
✅ Celery worker connects to Redis successfully
✅ Frontend starts without errors on port 5173
✅ You can visit [http://localhost:8000/docs](http://localhost:8000/docs) and see API documentation
✅ You can visit [http://localhost:5173](http://localhost:5173) and see the login page
✅ You can register a new account
✅ You can login and see the dashboard
✅ You can upload a file and see Work Order created
✅ WebSocket shows real-time agent progress
✅ Backend tests pass (`./test.sh`)
✅ Frontend tests pass (`./test.sh`)

---

**Happy coding! 🚀**

Upload your first Excel file and watch 30+ agents transform it into actionable insights. 📊
