# Full-Stack Starter Template

A production-ready, batteries-included template for building modern full-stack applications. Get started quickly with a pre-configured stack featuring FastAPI backend, React TypeScript frontend, database migrations, authentication, and comprehensive testing—all ready to customize for your specific needs.

## 🚀 What's Included

This template provides everything you need to start building a full-stack application:

- ✅ **Modern Backend** - FastAPI with async support, auto-generated API docs
- ✅ **Modern Frontend** - React 18+ with TypeScript and Tailwind CSS
- ✅ **Database Ready** - PostgreSQL with SQLAlchemy ORM and Alembic migrations
- ✅ **Authentication** - JWT-based auth with secure password hashing
- ✅ **Testing** - Comprehensive test suites for both frontend and backend
- ✅ **Developer Experience** - Hot reload, type safety, linting, and scripts
- ✅ **Production Ready** - Security best practices and deployment guides

## 📋 Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation
- **[pytest](https://pytest.org/)** - Testing framework
- **PostgreSQL** - Database (via Supabase)

### Frontend
- **[React 18+](https://react.dev/)** - UI library
- **[TypeScript](https://www.typescriptlang.org/)** - Type safety
- **[Vite](https://vitejs.dev/)** - Build tool
- **[Tailwind CSS](https://tailwindcss.com/)** - Styling
- **[React Router](https://reactrouter.com/)** - Routing
- **[Axios](https://axios-http.com/)** - HTTP client
- **[Jest](https://jestjs.io/)** - Testing framework

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (React + TypeScript)              │
│                                                              │
│  Pages → Components → Services → API Client                 │
│  (Auth, Dashboard)   (Reusable)  (Business)  (Axios)       │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
                      REST API (JSON)
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                   Backend (FastAPI + Python)                 │
│                                                              │
│  Routes → Services → Models → Database                       │
│  (Endpoints) (Logic) (ORM)   (PostgreSQL)                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🎯 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- A Supabase account (free tier works) or any PostgreSQL database

### 1. Clone This Template

```bash
git clone https://github.com/arunsaraswat/full-stack-starter.git your-app-name
cd your-app-name
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials
```

**Required environment variables (backend/.env):**
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```bash
# Run database migrations
./migrate.sh upgrade

# (Optional) Seed with sample data
./seed.sh
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.example .env
# Default values work for local development
```

### 4. Run the Application

**Option A: Run everything at once (recommended)**
```bash
# From project root
./run.sh
```

**Option B: Run separately in different terminals**
```bash
# Terminal 1 - Backend
cd backend
./start.sh

# Terminal 2 - Frontend
cd frontend
./start.sh
```

### 5. Access Your App

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc

## 📁 Project Structure

```
full-stack-starter/
├── backend/                    # Python FastAPI Backend
│   ├── alembic/               # Database migrations
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Config, security, dependencies
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Request/response schemas
│   │   ├── services/         # Business logic
│   │   ├── db/               # Database connection
│   │   └── main.py           # App entry point
│   ├── tests/                # Backend tests
│   ├── scripts/              # Utility scripts
│   ├── requirements.txt      # Python dependencies
│   └── *.sh                  # Helper scripts
│
├── frontend/                  # React TypeScript Frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── hooks/            # Custom React hooks
│   │   ├── context/          # React context providers
│   │   ├── types/            # TypeScript types
│   │   ├── utils/            # Utility functions
│   │   ├── App.tsx           # Main app component
│   │   └── main.tsx          # App entry point
│   ├── tests/                # Frontend tests
│   ├── package.json          # Node dependencies
│   ├── tailwind.config.js    # Tailwind configuration
│   └── vite.config.ts        # Vite configuration
│
├── docs/                      # Documentation
├── run.sh                     # Run full stack
└── README.md                  # You are here
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
./test.sh                    # Run all tests with coverage
./test.sh -v                 # Verbose output
./test.sh -k "test_name"     # Run specific test
```

### Run Frontend Tests
```bash
cd frontend
./test.sh                    # Run all tests with coverage
npm run test:watch           # Watch mode for development
```

**Coverage Goals:** Both frontend and backend target 70%+ test coverage.

## 🔧 Common Tasks

### Add a New API Endpoint

1. Create route handler in `backend/app/api/your_route.py`
2. Define Pydantic schemas in `backend/app/schemas/your_schema.py`
3. Add business logic in `backend/app/services/your_service.py`
4. Register route in `backend/app/main.py`
5. Write tests in `backend/tests/test_your_route.py`

### Add a New Frontend Page

1. Create page component in `frontend/src/pages/YourPage.tsx`
2. Add route in `frontend/src/App.tsx`
3. Create service methods in `frontend/src/services/yourService.ts`
4. Define TypeScript types in `frontend/src/types/index.ts`
5. Write tests in `frontend/tests/pages/YourPage.test.tsx`

### Database Migrations

```bash
cd backend

# Create a new migration
./migrate.sh create "add new table"

# Apply migrations
./migrate.sh upgrade

# Rollback last migration
./migrate.sh downgrade

# View migration history
./migrate.sh history
```

## 🔐 Security Features

- ✅ JWT token-based authentication
- ✅ bcrypt password hashing
- ✅ CORS middleware configured
- ✅ Environment variables for secrets
- ✅ SQL injection prevention (ORM)
- ✅ Input validation (Pydantic + client-side)
- ✅ Protected routes
- ⚠️ **IMPORTANT:** Change `SECRET_KEY` before deploying to production
- ⚠️ **IMPORTANT:** Use HTTPS in production
- ⚠️ **IMPORTANT:** Configure CORS allowed origins for production

## 📦 Available API Endpoints

### Public Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token
- `GET /health` - Health check

### Protected Endpoints (Require Authentication)
- `GET /api/users/profile` - Get current user profile
- `GET /api/dashboard` - Get dashboard data

See full API documentation at http://localhost:8000/docs when running locally.

## 🚢 Deployment

### Backend Deployment

**Environment Setup:**
1. Set all required environment variables
2. Change `SECRET_KEY` to a secure random value
3. Update `DATABASE_URL` to production database
4. Configure CORS allowed origins

**Run Migrations:**
```bash
./migrate.sh upgrade
```

**Production Server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Recommended Platforms:** Railway, Render, Fly.io, AWS, GCP, Azure

### Frontend Deployment

**Build for Production:**
```bash
cd frontend
npm run build
```

**Deploy the `dist/` folder to:**
- Vercel
- Netlify
- Cloudflare Pages
- AWS S3 + CloudFront
- Any static hosting service

**Environment Variables:**
Set `VITE_API_BASE_URL` to your production API URL.

## 🛠️ Customization

This is a template—make it your own! Here are some ideas:

- **Replace Authentication:** Swap JWT for OAuth, Auth0, or Firebase Auth
- **Add Features:** Payments (Stripe), email (SendGrid), file uploads (S3)
- **Change Database:** Switch from PostgreSQL to MySQL, MongoDB, etc.
- **Styling:** Replace Tailwind with styled-components, Emotion, or plain CSS
- **State Management:** Add Redux, Zustand, or Jotai if needed
- **API:** Convert to GraphQL, tRPC, or WebSockets

## 📚 Additional Documentation

- [Architecture Details](docs/architecture.md)
- [Database Schema](docs/database-schema.md)
- [API Examples](docs/api-examples.md)

## 🐛 Troubleshooting

### Backend Issues

**Database connection errors:**
- Verify `DATABASE_URL` in `backend/.env`
- Check database is running and accessible
- Ensure IP is whitelisted (if using Supabase)

**Import errors:**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Cannot connect to API:**
- Verify backend is running on port 8000
- Check `VITE_API_BASE_URL` in `frontend/.env`
- Look for CORS errors in browser console

**Build errors:**
- Delete `node_modules/` and reinstall: `rm -rf node_modules && npm install`
- Clear cache: `npm cache clean --force`
- Verify Node.js version: `node --version` (should be 18+)

## 🤝 Contributing

This is a template repository. Feel free to fork it and customize for your needs!

If you find bugs or have suggestions for the template itself, please open an issue.

## 📄 License

MIT License - Free to use for personal and commercial projects.

## ⭐ Getting Started Tips

1. **Start Simple:** Get the template running first before making changes
2. **Customize Gradually:** Change one thing at a time
3. **Read the Docs:** Check the `docs/` folder for more details
4. **Use the Tests:** Run tests frequently to catch issues early
5. **Environment Variables:** Never commit `.env` files to git

## 🎉 What to Build?

This template is perfect for:

- SaaS applications
- Internal tools and dashboards
- MVPs and prototypes
- API-driven applications
- Portfolio projects
- Learning full-stack development

---

**Ready to build something awesome? Start coding! 🚀**
