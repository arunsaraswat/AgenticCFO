# Agentic CFO Platform

**A CFO that never sleeps** — An Excel-first, multi-agent financial automation platform that delivers cash forecasting, margin analysis, rolling forecasts, capital allocation, and embedded controls—all from uploaded spreadsheets.

[![Version](https://img.shields.io/badge/version-0.2--excel--first-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![React](https://img.shields.io/badge/react-18+-61DAFB)]()
[![Build Status](https://img.shields.io/badge/build-MVP_phase-yellow)]()

---

## 📚 Documentation & Planning

- **[Implementation Plan](./docs/implementation-plan.md)** - Complete 22-week roadmap (MVP + Full Build)
- **[MVP Roadmap](./docs/mvp-roadmap.md)** - 2-week MVP quick reference guide
- **[Progress Tracker](./PROGRESS.md)** - Current build status and metrics
- **[Architecture Deep-Dive](./docs/architecture.md)** - Comprehensive technical design
- **[Database Schema](./docs/database-schema.md)** - Full schema documentation
- **[Development Guide](./CLAUDE.md)** - Setup, patterns, and best practices

**Current Status:** 🟡 MVP Phase - Work order system + file upload UI complete, integrating frontend

---

## 🎯 Vision

Ship a supervised **mesh of finance agents** orchestrated by **LangGraph** that process Excel/CSV files to deliver:

- **13-week cash forecasting** with liquidity warnings
- **Day-3 month-end close** with auto-reconciliations
- **Margin bridges** and variance explanations (Price/Volume/Mix)
- **Rolling forecasts** and capital allocation rankings (EVA/NPV/IRR)
- **Policy-as-code** enforcement with immutable audit trails

**No integrations required.** Upload the Excel files you already export from your ERP/bank/POS systems, and agents do the rest.

---

## 🚀 What Makes This Different

### Excel-First Approach
- **Zero mandatory integrations** — All insights run from uploaded files
- **Template catalog** with mapping memory learns your column names
- **Workbook Auditor** scans for macros, external links, hidden sheets
- **Dataset versioning** tracks every upload with full lineage

### Agentic Architecture
- **30+ specialized agents** for treasury, R2R, FP&A, controls, and industry-specific tasks
- **LangGraph orchestration** with human-above-the-loop approval gates
- **Multi-model LLM strategy** (GPT-4 for reasoning, Claude-3.5 for analysis, GPT-3.5 for routine tasks)
- **Guardrail & Critic agents** enforce policies and validate outputs

### Production-Ready Controls
- **Policy-as-code:** Materiality thresholds, SoD checks, treasury limits
- **Immutable audit logs:** Who, what, when, why—for every action
- **Evidence bundles:** ZIP exports with artifacts + logs + policy versions
- **Explainable AI:** Every agent provides reasoning traces and confidence scores

---

## 📋 Key Features

### 1. File Intake Gateway
- **Multi-channel ingestion:** Web upload, SFTP drop box, email inbox
- **Virus scanning** and macro stripping
- **Template detection:** Auto-identifies TrialBalance, AP_OpenItems, POS_Sales, etc.
- **Mapping Studio:** Semantic column matching with mapping memory

### 2. Agent Network (30+ Agents)

#### Treasury & Working Capital
- **Cash Commander:** 13-week forecasts, liquidity alerts, covenant checks
- **Receivables Radar:** DSO optimization, collection prioritization
- **Payables Protector:** Duplicate detection, early-pay ROI, terms optimization

#### Record-to-Report & Performance
- **Close Copilot:** Auto-recs, accruals, Day-3 close status
- **Margin Mechanic:** P/V/M bridges, inflation vs. productivity analysis
- **Cost Genome:** Vendor taxonomy, consolidation opportunities

#### FP&A & Capital Allocation
- **Forecast Factory:** Rolling forecasts, scenario trees, variance explanations
- **Portfolio Allocator:** EVA/NPV/IRR ranking, risk-adjusted screens
- **Deal Diligence:** M&A valuation, integration risk assessment

#### Controls & Compliance
- **Guardrail:** Policy enforcement (SoD, limits, materiality)
- **Critic:** Statistical validation, outlier detection
- **Compliance Scribe:** Audit logs, evidence bundles
- **Workbook Auditor:** Spreadsheet risk assessment

#### Industry-Specific Agents
- **Retail:** GMROI Optimizer, Promo ROI, Assortment, Store & Labor
- **Energy:** CFaR Analyst, Hedge Strategist, Turnaround Planner, Emissions Accountant

### 3. Orchestration (LangGraph)
- **Work Order Graph:** Routes uploaded files through agent networks
- **State persistence:** PostgreSQL checkpointing for resumable workflows
- **Approval gates:** Human-above-the-loop reviews at defined checkpoints
- **Real-time updates:** WebSocket progress tracking

### 4. Outputs & Artifacts
- **Excel artifacts:** Cash_Ladder.xlsx, GM_Bridge_BU_SKU.xlsx, Portfolio_Ranked.xlsx
- **PDF reports:** Liquidity_Warnings.pdf, Covenant_Report.pdf
- **Investment memos:** Auto-generated Word documents
- **Evidence bundles:** ZIP exports with full lineage for auditors

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 FRONTEND (React + TypeScript)                │
│   Upload Wizard │ Mapping Studio │ CFO Dashboard            │
│                 WebSocket Real-Time Updates                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                 BACKEND (FastAPI + Python)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FILE INTAKE GATEWAY                                 │  │
│  │  Upload API → Workbook Auditor → Mapping Studio     │  │
│  │  → DQ Validator → Dataset Staging (Versioned)       │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │  LANGGRAPH ORCHESTRATION                            │  │
│  │  DQ → Routing → Agent Network → Guardrail →        │  │
│  │  Critic → Approval Gate → Artifact Generation      │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │  AGENT NETWORK (30+ Specialized Agents)            │  │
│  │  Treasury │ R2R │ FP&A │ Controls │ Industry       │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │  LLM LAYER (OpenRouter Multi-Model)                 │  │
│  │  GPT-4 │ Claude-3.5 │ GPT-3.5 │ Llama-3.1         │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │  OUTPUT & AUDIT LAYER                               │  │
│  │  Artifacts (Excel/PDF/Word) │ Immutable Logs       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

Infrastructure: PostgreSQL/Supabase │ Redis (Celery) │ ChromaDB │ WebSockets
```

See [docs/architecture.md](docs/architecture.md) for detailed technical design.

---

## 📦 Tech Stack

### Backend (Python/FastAPI)
- **Orchestration:** LangGraph 0.2+, LangChain 0.3+
- **LLMs:** OpenRouter API (GPT-4, Claude-3.5, GPT-3.5, Llama-3.1)
- **Data Processing:** Pandas 2.1+, Polars 0.20+, OpenPyXL 3.1+
- **Database:** PostgreSQL 15+ / Supabase, Redis 7.0+
- **Task Queue:** Celery 5.3+ (async agent execution)
- **Vector Store:** ChromaDB 0.4+ (mapping memory)
- **Web Framework:** FastAPI 0.109+, Uvicorn
- **Auth:** JWT tokens (python-jose), bcrypt 4.1+

### Frontend (React/TypeScript)
- **Core:** React 18+, TypeScript 5.3+, Vite 5+
- **Styling:** Tailwind CSS 3.4+, Headless UI
- **State:** React Context, React Query (optional)
- **API:** Axios 1.6+, Native WebSocket API
- **Testing:** Jest 29+, React Testing Library

### Infrastructure
- **Database:** Supabase PostgreSQL (hosted)
- **Caching:** Redis (for Celery + session cache)
- **File Storage:** Local filesystem (→ S3 in future)
- **Deployment:** Railway/Render (backend), Vercel/Netlify (frontend)

---

## 🎬 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase account (free tier works)
- OpenRouter API key ([openrouter.ai](https://openrouter.ai))
- Redis server (local or cloud)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/AgenticCFO.git
cd AgenticCFO
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials:
#   DATABASE_URL=<your-supabase-connection-string>
#   OPENROUTER_API_KEY=<your-openrouter-key>
#   REDIS_URL=redis://localhost:6379/0
#   SECRET_KEY=<generate-secure-key>

# Run migrations
./migrate.sh upgrade

# Optional: Seed with test data
./seed.sh
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment (optional, defaults work for local)
cp .env.example .env
```

### 4. Start Services

**Option A: Run everything at once**
```bash
# From project root
./run.sh
```

**Option B: Run separately**
```bash
# Terminal 1 - Backend
cd backend
./start.sh

# Terminal 2 - Celery worker (for async agent tasks)
cd backend
celery -A app.tasks.celery_app worker --loglevel=info

# Terminal 3 - Frontend
cd frontend
./start.sh
```

### 5. Access Application
- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Project Structure

```
AgenticCFO/
├── backend/                        # Python FastAPI Backend
│   ├── alembic/                   # Database migrations
│   ├── app/
│   │   ├── agents/                # 30+ Finance agents
│   │   │   ├── treasury/          # Cash Commander, Receivables Radar, etc.
│   │   │   ├── r2r/               # Close Copilot, Margin Mechanic
│   │   │   ├── fpa/               # Forecast Factory, Portfolio Allocator
│   │   │   ├── control/           # Guardrail, Critic, Compliance Scribe
│   │   │   └── industry/          # Retail, Energy-specific agents
│   │   ├── orchestration/         # LangGraph workflows
│   │   │   ├── work_order_graph.py
│   │   │   ├── state.py
│   │   │   └── nodes.py
│   │   ├── intake/                # File ingestion
│   │   │   ├── uploader.py
│   │   │   ├── template_catalog.py
│   │   │   ├── mapping_studio.py
│   │   │   └── workbook_auditor.py
│   │   ├── data_quality/          # DQ validators & reconcilers
│   │   ├── policy/                # Policy engine
│   │   ├── artifacts/             # Output generation
│   │   ├── api/                   # FastAPI endpoints
│   │   ├── core/                  # Config, security, dependencies
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # Business logic
│   │   ├── db/                    # Database session
│   │   └── main.py                # App entry point
│   ├── tests/                     # Backend tests
│   ├── requirements.txt           # Python dependencies
│   └── *.sh                       # Helper scripts
│
├── frontend/                      # React TypeScript Frontend
│   ├── src/
│   │   ├── components/            # React components
│   │   │   ├── upload/            # Upload Wizard
│   │   │   ├── mapping/           # Mapping Studio
│   │   │   ├── dashboard/         # CFO Dashboard
│   │   │   └── work-orders/       # Work Order tracking
│   │   ├── pages/                 # Page components
│   │   ├── services/              # API services
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── context/               # React context providers
│   │   ├── types/                 # TypeScript types
│   │   └── utils/                 # Utility functions
│   ├── tests/                     # Frontend tests
│   ├── package.json               # Node dependencies
│   └── *.config.js/ts             # Build configs
│
├── docs/                          # Documentation
│   ├── architecture.md            # Detailed architecture (THIS IS COMPREHENSIVE!)
│   ├── database-schema.md         # Database design
│   └── api-examples.md            # API usage examples
│
├── README.md                      # This file
├── PROJECT_SUMMARY.md             # Project overview
├── SETUP.md                       # Quick setup guide
└── run.sh                         # Main launcher script
```

---

## 🎓 Example Workflows

### Workflow 1: Close-to-Forecast (Monthly)

**Upload:**
- `TrialBalance.xlsx`
- `JE_Detail.csv`
- `BankStatement.csv`
- `AR_OpenItems.xlsx`
- `AP_OpenItems.xlsx`

**Agent Execution:**
1. **DQ Validation** checks TB balances, bank-to-GL reconciliation
2. **Close Copilot** auto-recs accounts, proposes accruals
3. **Margin Mechanic** builds P/V/M bridges
4. **Forecast Factory** rolls forward using actuals + drivers
5. **Critic** challenges outliers, flags low-confidence
6. **Guardrail** enforces materiality thresholds
7. **Compliance Scribe** compiles audit binder

**Outputs:**
- `Close_Status.xlsx` (Day-3 checklist)
- `Auto_Recs.xlsx` (bank, AR/AP reconciliations)
- `GM_Bridge_BU_SKU.xlsx` (margin waterfalls)
- `Forecast_Rolling.xlsx` (12-month forecast)
- `Audit_Binder.zip` (evidence bundle)

**SLOs:** Day-3 close achieved; ≥80% recs auto-cleared; ≥95% GM variance explained

---

### Workflow 2: Cash Control (Weekly)

**Upload:**
- `BankStatement_Week12.csv`
- `AP_OpenItems_Week12.xlsx`
- `AR_OpenItems_Week12.xlsx`
- `Payments_Executed_Week12.csv`

**Agent Execution:**
1. **DQ Validation** checks positive pay, duplicate payments
2. **Cash Commander** creates 13-week forecast with Monte Carlo confidence intervals
3. **Receivables Radar** scores invoices by collection risk
4. **Payables Protector** detects duplicates, calculates early-pay ROI
5. **Covenant Keeper** checks debt covenant headroom
6. **Guardrail** validates treasury limits, SoD on payments
7. **Critic** compares to prior forecast, explains variances

**Outputs:**
- `Cash_Ladder.xlsx` (13-week forecast)
- `Liquidity_Warnings.pdf` (covenant alerts)
- `Collections_Prioritized.xlsx` (AR risk scores)
- `Duplicates_Flagged.xlsx` (payment duplicates)

**SLOs:** T+1 bank rec ≥99%; duplicate detection ≥95% precision; cash MAPE ≤10% @ 2-week

---

### Workflow 3: Capital Allocation (Quarterly)

**Upload:**
- `Project_Cases.xlsx` (cashflows, risks, synergies)
- `WACC_Policy.xlsx` (cost of capital by division)
- `Capacity_Constraints.xlsx` (budget, resources, gates)

**Agent Execution:**
1. **DQ Validation** checks NPV inputs, discount rates
2. **Portfolio Allocator** ranks projects by EVA/NPV/IRR
3. **Critic** validates DCF assumptions, runs sensitivity
4. **Guardrail** applies policy gates (hurdle rates, payback limits)
5. **Deal Diligence** (if M&A) triangulates valuation
6. **Compliance Scribe** logs ranking decisions, policy versions

**Outputs:**
- `Portfolio_Ranked.xlsx` (EVA-ranked projects)
- `Investment_Memos.docx` (one-pagers per project)
- `Sensitivity_Tornado.xlsx` (risk analysis)

**SLOs:** 100% projects policy-compliant; EVA/NPV/IRR + downside case

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
./test.sh                 # All tests with coverage
./test.sh -v              # Verbose output
./test.sh -k test_agent   # Run specific test
```

**Coverage target:** 70%+

### Run Frontend Tests
```bash
cd frontend
./test.sh                 # All tests with coverage
npm run test:watch        # Watch mode for development
```

**Coverage target:** 70%+

---

## 🔐 Security Features

### Data Protection
- **TLS 1.3** for all API traffic
- **At-rest encryption** (Supabase default)
- **JWT authentication** with bcrypt password hashing
- **Tenant isolation** via PostgreSQL row-level security

### Audit & Compliance
- **Immutable audit log** (append-only table)
- **Full dataset lineage** (input → processing → output)
- **Approval history** with timestamps and rationale
- **Policy version tracking** (effective dates)

### Spreadsheet Risk Mitigation
- **Workbook Auditor** scans all uploads for:
  - Macros (stripped by default)
  - External links (flagged)
  - Hidden sheets (reported)
  - Volatile formulas (NOW(), RAND())
- High-risk workbooks **quarantined** from payment flows

### Policy-as-Code
- **Materiality thresholds** enforced by Guardrail
- **Segregation of Duties (SoD)** violations detected
- **Treasury limits** validated (min cash, max exposure)
- **Disclosure gates** applied per policy pack

---

## 📊 Success Metrics

### Technical SLOs
- **Ingestion latency:** ≤10 min per 100MB file
- **Mapping reuse:** ≥90% after first cycle
- **Day-3 close:** Achieved for 2+ consecutive months
- **Bank reconciliation:** T+1 coverage ≥99%
- **Duplicate detection:** ≥95% precision, ≥85% recall
- **Control logging:** 100% actions logged

### Agent Performance
- **Cash forecast MAPE:** ≤10% @ 2-week horizon
- **Revenue forecast MAPE:** ≤8% @ 90-day horizon
- **Margin bridge:** ≥95% of GM delta explained
- **Auto-rec clearance:** ≥80% of reconciliations

### User Experience
- **Upload-to-insight:** ≤30 min median
- **Exception resolution:** ≤24 hrs P50
- **User satisfaction:** ≥4.0/5.0

---

## 🛠️ Configuration

### Environment Variables (Backend)

**Required:**
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# OpenRouter (LLMs)
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_DEFAULT_MODEL=openai/gpt-4-turbo

# Redis (Celery)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ChromaDB
CHROMA_PERSIST_DIRECTORY=/var/agenticcfo/chroma

# File Storage
ARTIFACTS_STORAGE_PATH=/var/agenticcfo/artifacts
MAX_UPLOAD_SIZE_MB=500
```

**Optional:**
```env
# LangSmith (debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=agenticcfo

# Supabase (if using for caching)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Sentry (error tracking)
SENTRY_DSN=your-sentry-dsn

# CORS
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### Environment Variables (Frontend)

```env
VITE_API_BASE_URL=http://localhost:8000  # Backend URL
```

---

## 🚢 Deployment

### Backend Deployment

**Environment Setup:**
1. Set all required environment variables
2. Change `SECRET_KEY` to a secure random value: `openssl rand -hex 32`
3. Update `DATABASE_URL` to production database (Supabase hosted)
4. Configure `CORS_ORIGINS` for your frontend domain
5. Set `OPENROUTER_API_KEY` for LLM access
6. Set `REDIS_URL` for Celery task queue

**Run Migrations:**
```bash
./migrate.sh upgrade
```

**Production Server:**
```bash
# Option 1: Uvicorn (single worker)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Option 2: Gunicorn with Uvicorn workers (recommended)
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Celery Workers (async agents):**
```bash
celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4
```

**Recommended Platforms:** Railway, Render, Fly.io, AWS ECS, GCP Cloud Run

---

### Frontend Deployment

**Build for Production:**
```bash
cd frontend
npm run build  # Creates dist/ folder
```

**Deploy `dist/` folder to:**
- **Vercel:** Zero-config deployment
- **Netlify:** Drag-drop or CLI
- **Cloudflare Pages:** Fast global CDN
- **AWS S3 + CloudFront:** S3 static hosting + CDN

**Environment Variables:**
Set `VITE_API_BASE_URL` to your production backend URL.

---

## 📚 Documentation

- **[Architecture](docs/architecture.md)** - Comprehensive technical design (recommended read!)
- **[Database Schema](docs/database-schema.md)** - Database tables and relationships
- **[API Examples](docs/api-examples.md)** - API endpoint usage examples
- **[Setup Guide](SETUP.md)** - Quick 5-minute setup instructions
- **[Project Summary](PROJECT_SUMMARY.md)** - High-level project overview

---

## 🐛 Troubleshooting

### Backend Issues

**Database connection failed:**
- Verify `DATABASE_URL` in `backend/.env`
- Check Supabase project is active
- Ensure IP whitelisted in Supabase settings

**Import errors:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Redis connection failed:**
```bash
# Start Redis locally
redis-server

# Or use Redis Cloud URL in .env
```

**OpenRouter API errors:**
- Verify `OPENROUTER_API_KEY` is set correctly
- Check API credits at [openrouter.ai](https://openrouter.ai)
- Review rate limits for your models

### Frontend Issues

**Cannot connect to API:**
- Verify backend is running on port 8000
- Check `VITE_API_BASE_URL` in `frontend/.env`
- Look for CORS errors in browser console

**Build errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Agent Issues

**LangGraph execution hangs:**
- Check Celery worker is running
- Review Redis connection
- Check LangSmith traces (if enabled)

**Low confidence scores:**
- Review agent reasoning traces in work order logs
- Validate input data quality (DQ reports)
- Check if policy constraints are too strict

---

## 🤝 Contributing

This project is under active development. Contributions welcome!

**Areas for contribution:**
- Additional industry agents (Manufacturing, Healthcare)
- New template definitions (Payroll, Inventory)
- Frontend UI/UX improvements
- Documentation and examples
- Test coverage expansion

---

## 📄 License

MIT License - Free to use for personal and commercial projects.

---

## 🎉 What to Build?

This platform is perfect for:

- **CFO offices** looking to automate financial analysis
- **Finance teams** needing fast close and rolling forecasts
- **Treasury departments** managing cash and covenants
- **FP&A analysts** running scenarios and capital allocation
- **Controllers** seeking audit-ready evidence
- **Retail finance** teams optimizing GMROI and promotions
- **Energy finance** managing hedge strategies and production economics

---

## 🌟 Key Differentiators

1. **Excel-First, Not API-First**
   - No mandatory system integrations
   - Works with files you already export
   - Mapping memory learns your column names

2. **Agentic, Not Rule-Based**
   - 30+ specialized AI agents (not static dashboards)
   - Explains variances, recommends actions
   - Adapts to your data patterns

3. **Controls-First, Not Data-First**
   - Policy-as-code guardrails
   - Immutable audit logs
   - Human-above-the-loop approvals

4. **Industry-Specific, Not Generic**
   - Retail pack (GMROI, promo ROI, assortment)
   - Energy pack (CFaR, hedge strategy, emissions)
   - More industries coming (Manufacturing, Healthcare)

---

## 📞 Support

For questions, issues, or feature requests:
- **GitHub Issues:** [github.com/yourrepo/AgenticCFO/issues](https://github.com/yourrepo/AgenticCFO/issues)
- **Email:** support@agenticcfo.com
- **Docs:** [docs.agenticcfo.com](https://docs.agenticcfo.com)

---

## 🚀 Ready to Build?

```bash
# Clone and run in 5 minutes
git clone https://github.com/yourrepo/AgenticCFO.git
cd AgenticCFO
./run.sh
```

**Start coding!**

Upload your first Excel file and watch agents transform it into insights. 📊
