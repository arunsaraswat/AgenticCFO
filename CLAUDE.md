# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Custom Claude Code Agents

This project includes specialized subagents for code review and testing:

- **`/architect-review`** - Reviews code for architectural alignment, FastAPI best practices, security, and design patterns
- **`/tester-review`** - Analyzes test coverage and generates missing test implementations

See [`.claude/README.md`](.claude/README.md) for detailed usage instructions.

**Recommended Workflow:**
1. Implement feature → 2. Run `/architect-review` → 3. Fix issues → 4. Run `/tester-review` → 5. Implement tests → 6. Commit

## Project Overview

**Agentic CFO Platform** is an Excel-first, multi-agent financial automation system powered by LangGraph orchestration. The platform processes uploaded Excel/CSV files through 30+ specialized finance agents to deliver cash forecasting, margin analysis, rolling forecasts, capital allocation, and compliance—without requiring system integrations.

**Core Architecture:** FastAPI (Python) backend + React (TypeScript) frontend + LangGraph agent orchestration + OpenRouter multi-model LLMs + PostgreSQL/Supabase + Redis/Celery + ChromaDB vector store.

## Development Commands

### Full Stack

```bash
# Start everything (backend + frontend + migrations)
./run.sh

# The script automatically:
# - Checks dependencies
# - Runs database migrations
# - Starts backend on port 8000
# - Starts frontend on port 5173
```

### Backend (FastAPI)

```bash
cd backend

# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start development server
./start.sh
# Or manually: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Database migrations
./migrate.sh upgrade              # Apply all pending migrations
./migrate.sh create "message"     # Create new migration
./migrate.sh downgrade            # Rollback last migration
./migrate.sh history              # Show migration history
./migrate.sh current              # Show current migration

# Testing
./test.sh                         # Run all tests with coverage
./test.sh -v                      # Verbose output
./test.sh -k test_name            # Run specific test
pytest tests/test_auth.py         # Run specific file
pytest tests/test_auth.py::test_login  # Run specific test function

# Code quality
black .                           # Format code
flake8                           # Lint
mypy app                         # Type checking
```

### Frontend (React + TypeScript)

```bash
cd frontend

# Setup
npm install

# Development
npm run dev                       # Start dev server (port 5173)
npm run build                     # Production build
npm run preview                   # Preview production build

# Testing
./test.sh                         # Run all tests with coverage
npm run test:watch                # Watch mode for development
npm test                          # Run tests once

# Code quality
npm run lint                      # ESLint
```

## High-Level Architecture

### Multi-Agent Orchestration System

The platform is built around **5 architectural layers** that process uploaded files through specialized agents:

#### Layer 1: File Intake Gateway
**Location:** `backend/app/intake/` (future implementation)

- **Upload API** (`/api/intake/upload`): Multi-channel ingestion (web, SFTP, email)
- **Workbook Auditor Agent**: Scans Excel files for macros, external links, hidden sheets, volatile formulas
- **Template Catalog**: Recognizes file types (TrialBalance, AP_OpenItems, POS_Sales, etc.)
- **Mapping Studio**: Semantic column matching using ChromaDB embeddings
- **Data Quality Validator**: Pre-flight checks, cross-file reconciliations
- **Dataset Versioning**: Every upload creates immutable versioned snapshot in PostgreSQL

**Key Concept:** Files are never modified. Each upload creates a new dataset version with full lineage tracking.

#### Layer 2: LangGraph Orchestration
**Location:** `backend/app/orchestration/` (future implementation)

**Work Order State Graph Pattern:**
```
START → DQ Validation → Routing → Agent Network → Guardrail → Critic → Approval Gate → Artifact Gen → END
```

**State Management:**
- Each uploaded file triggers a **Work Order** (stored in `work_orders` table)
- Work Order contains: `{objective, input_datasets[], policy_refs[], agent_outputs{}, approval_gates[], artifacts[]}`
- State persisted to PostgreSQL via LangGraph checkpointing
- Enables resumable workflows and human-above-the-loop approvals

**Critical Implementation Details:**
- Use `langgraph.graph.StateGraph` with `PostgresSaver` for checkpointing
- Define `WorkOrderState` as TypedDict with all required fields
- Each node function receives state, updates it, returns modified state
- Conditional edges route to different agents based on objective keywords
- `approval_gate_node` uses LangGraph's interrupt mechanism to pause execution

#### Layer 3: Agent Network (30+ Specialized Agents)
**Location:** `backend/app/agents/` (future implementation)

**Base Agent Pattern:**
```python
class BaseFinanceAgent(ABC):
    def __init__(self, agent_name, model_name, tools):
        self.llm = ChatOpenAI(base_url="https://openrouter.ai/api/v1", model=model_name)
        self.agent = create_openai_functions_agent(llm, tools, prompt)

    async def execute(self, inputs, policy_constraints, progress_callback) -> AgentOutput:
        # Returns: {output, confidence_score, artifacts[], reasoning_trace[], execution_time, cost_usd}
```

**Agent Categories:**
- **Treasury** (`agents/treasury/`): Cash Commander, Receivables Radar, Payables Protector, Covenant Keeper
- **R2R** (`agents/r2r/`): Close Copilot, Margin Mechanic, Cost Genome
- **FP&A** (`agents/fpa/`): Forecast Factory, Portfolio Allocator, Deal Diligence
- **Controls** (`agents/control/`): Guardrail, Critic, Compliance Scribe, Workbook Auditor
- **Industry** (`agents/industry/`): Retail (GMROI, Promo ROI), Energy (CFaR, Hedge)

**LangChain Tool Pattern:**
All agents use LangChain `Tool` objects that wrap Python functions:
```python
Tool(
    name="analyze_bank_statement",
    func=self._analyze_bank_statement,
    description="Analyze bank statement to extract cash positions. Input: dataset_id (UUID)"
)
```

**OpenRouter Multi-Model Strategy:**
- **GPT-4 Turbo** (`openai/gpt-4-turbo`): Complex reasoning (Portfolio Allocator, Cash Commander)
- **Claude-3.5 Sonnet** (`anthropic/claude-3.5-sonnet`): Data analysis (Margin Mechanic, Critic)
- **GPT-3.5 Turbo** (`openai/gpt-3.5-turbo`): Routine tasks (Guardrail, Workbook Auditor)
- **Llama-3.1 70B** (`meta-llama/llama-3.1-70b-instruct`): Cost optimization for bulk processing

#### Layer 4: LLM & Tool Layer
**Location:** `backend/app/tools/` (future implementation)

**Custom Finance Tools:**
- `calculate_npv`: NPV/IRR/payback period for capital projects
- `calculate_wacc`: WACC calculator for capital allocation
- `analyze_variance`: Statistical variance decomposition
- `monte_carlo_simulation`: Cash forecast confidence intervals

**ChromaDB Integration:**
- **Purpose:** Semantic column mapping memory
- **Collection:** `column_mappings` with embeddings
- **Usage:** `find_similar_columns(source_column, template_type)` returns top-k matches
- **Storage:** Persisted to `CHROMA_PERSIST_DIRECTORY` env var

#### Layer 5: Output & Audit Layer
**Location:** `backend/app/artifacts/` (future implementation)

**Artifact Types:**
- **Excel** (via `openpyxl`): Cash_Ladder.xlsx, GM_Bridge_BU_SKU.xlsx, Portfolio_Ranked.xlsx
- **PDF** (via `reportlab`): Liquidity_Warnings.pdf, Covenant_Report.pdf
- **Word** (via `python-docx`): Investment_Memos.docx

**Audit Trail (PostgreSQL):**
- `audit_events` table: Append-only event log
- `datasets` table: Full lineage (input → processing → output)
- `work_orders.execution_log`: Immutable JSONB array of state transitions
- `artifacts` table: Checksum (SHA-256) for integrity verification

### Database Architecture

**Core Tables:**
```sql
-- Multi-tenancy
tenants (id, name, slug, settings, is_active)
users (id, email, tenant_id, role, approval_authority)

-- File ingestion
file_uploads (id, tenant_id, filename, file_hash, upload_channel, workbook_risk_score, status)
datasets (id, tenant_id, template_type, entity, period_start/end, version, data_hash, mapping_config_id, dq_status)
mapping_configs (id, tenant_id, template_type, column_mappings::JSONB, date_formats::JSONB, use_count)

-- Orchestration
work_orders (id, tenant_id, objective, input_datasets::JSONB, agent_outputs::JSONB, guardrail_checks::JSONB,
             approval_gates::JSONB, artifacts::JSONB, execution_log::JSONB)
policy_packs (id, tenant_id, version, policy_data::JSONB, effective_from/to)

-- Output
artifacts (id, work_order_id, artifact_type, file_path, checksum_sha256)
audit_events (id, tenant_id, work_order_id, event_type, details::JSONB, timestamp)
```

**Key Patterns:**
- **Versioning:** Datasets have `(tenant_id, template_type, entity, period_start, version)` unique constraint
- **Lineage:** Every artifact references exact dataset IDs via work_order → input_datasets
- **Immutability:** `audit_events` is append-only (no updates/deletes)
- **JSONB columns:** Used for flexible schemas (agent outputs, policy rules, execution logs)

### Real-Time WebSocket Updates

**Pattern:**
```python
# Backend: app/websocket/manager.py
manager = ConnectionManager()  # {tenant_id: {user_id: WebSocket}}

# Send progress updates from agent nodes
await manager.send_agent_progress(tenant_id, work_order_id, agent_name, progress_pct, current_step)

# Frontend: hooks/useWorkOrderUpdates.ts
const { updates, agentProgress, connected } = useWorkOrderUpdates(workOrderId)
// Real-time updates via native WebSocket API
```

**Message Types:**
- `work_order_update`: Stage changes, agent completions, approval requests
- `agent_progress`: Percentage + current step (e.g., "Analyzing bank statement...")
- `heartbeat`: Keep-alive ping every 30 seconds

### Policy-as-Code Enforcement

**Flow:**
1. `Policy_Pack.xlsx` uploaded and parsed into `policy_packs` table (JSONB)
2. Each Work Order references `policy_refs: ["Policy_Pack_V3#Treasury", "Policy_Pack_V3#Materiality"]`
3. **Guardrail Agent** enforces at graph checkpoints:
   - Materiality thresholds (e.g., variances >$100K require explanation)
   - Segregation of Duties (SoD) violations (e.g., same user can't approve own payments)
   - Treasury limits (e.g., min cash balance, max FX exposure)
   - Disclosure gates (e.g., revenue recognition criteria)
4. Violations create `pending_approvals` entry in Work Order state
5. LangGraph pauses at `approval_gate_node` until human approval/override

**Guardrail Output:**
```python
{
  "check_name": "minimum_cash_balance",
  "status": "failed",  # or "passed"
  "severity": "critical",  # "critical", "high", "medium", "low"
  "reason": "Cash balance $450K below policy minimum $500K",
  "recommended_action": "Accelerate AR collections or arrange credit line"
}
```

## Current State vs. Future Implementation

**✅ Currently Implemented:**
- Backend foundation: FastAPI + SQLAlchemy + Alembic migrations
- Frontend foundation: React + TypeScript + Vite
- Authentication: JWT tokens, bcrypt password hashing
- Database: User management, basic CRUD
- Testing frameworks: pytest (backend), jest (frontend)

**🚧 To Be Implemented (per docs/architecture.md):**
- File Intake Gateway (upload API, Workbook Auditor, Mapping Studio, DQ validators)
- LangGraph orchestration (Work Order Graph, state management, approval gates)
- 30+ specialized agents (Cash Commander, Close Copilot, Margin Mechanic, etc.)
- OpenRouter LLM integration
- ChromaDB vector store for mapping memory
- Celery + Redis for async agent execution
- WebSocket server for real-time progress
- Artifact generation (Excel/PDF/Word)
- Policy engine and Guardrail/Critic agents

**Implementation Roadmap:** See docs/architecture.md → "Implementation Roadmap" (6 phases, 24 weeks)

## Key Environment Variables

**Backend (`backend/.env`):**
```env
# Required
DATABASE_URL=postgresql://user:password@host:5432/dbname
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here

# Agent Configuration
OPENROUTER_DEFAULT_MODEL=openai/gpt-4-turbo
CHROMA_PERSIST_DIRECTORY=/var/agenticcfo/chroma
ARTIFACTS_STORAGE_PATH=/var/agenticcfo/artifacts

# Optional (debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=agenticcfo
```

**Frontend (`frontend/.env`):**
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Architecture Decision Records

### Why LangGraph over CrewAI/AutoGen?
- **Graph-based workflows** → Perfect for Work Order routing with conditional paths
- **State persistence** → PostgreSQL checkpointing enables resumable workflows
- **Cyclic execution** → Supports Guardrail → Agent → Critic → Agent feedback loops
- **Human-in-loop** → Native interrupt mechanism for approval gates
- **Explainability** → Full execution trace in state.execution_log

### Why OpenRouter over Direct OpenAI/Anthropic?
- **Multi-model flexibility** → Switch between GPT-4, Claude-3.5, Llama without code changes
- **Cost optimization** → Route routine tasks to cheaper models
- **Redundancy** → If one provider has outage, fallback to others
- **Single API** → Unified interface for 100+ models

### Why Excel-First (No Mandatory Integrations)?
- **Time-to-value** → Works with files clients already export from ERPs
- **Trust-building** → Prove value before asking for system access
- **Flexibility** → Not locked into specific ERP/accounting platforms
- **Connectors as optimization** → Can add later without re-architecting agents

### Why Celery for Agent Execution?
- **Async processing** → Don't block API requests while agents run (5-15 min)
- **Scalability** → Horizontal scaling via worker pool
- **Retry logic** → Automatic retries with exponential backoff
- **Progress tracking** → Integrate with WebSocket for real-time updates

## Testing Strategy

**Backend:**
- **Unit tests:** Individual agent logic, tool functions, validators
- **Integration tests:** API endpoints, database operations, LangGraph workflows
- **Agent tests:** Mock LLM responses, verify tool calls, validate output schemas
- **Coverage target:** 70%+

**Frontend:**
- **Component tests:** React Testing Library for UI components
- **Integration tests:** User flows (login, upload, view work orders)
- **E2E tests:** (Future) Playwright for full workflows
- **Coverage target:** 70%+

## Common Patterns

### Adding a New Agent

1. **Create agent class** in `backend/app/agents/{category}/new_agent.py`:
```python
class NewAgent(BaseFinanceAgent):
    def get_system_prompt(self) -> str:
        return "You are {role}. Your responsibilities: {list}."

    def get_default_tools(self) -> List[Tool]:
        return [Tool(name="tool_name", func=self._tool_func, description="...")]

    def _prepare_input(self, inputs, policy_constraints) -> Dict:
        # Format inputs for agent

    def _parse_output(self, raw_output) -> Dict:
        # Extract structured data from LLM response

    async def _generate_artifacts(self, parsed_output) -> List[Dict]:
        # Generate Excel/PDF/Word artifacts
```

2. **Add to agent registry** in `backend/app/agents/__init__.py`
3. **Update routing logic** in `backend/app/orchestration/nodes.py` → `routing_node()`
4. **Create tests** in `backend/tests/test_agents/test_new_agent.py`
5. **Update AGENT_MODEL_MAP** in `backend/app/orchestration/config.py`

### Creating a Database Migration

```bash
cd backend
./migrate.sh create "add work_orders table"
# Edit generated file in alembic/versions/
# Add upgrade() and downgrade() logic
./migrate.sh upgrade
```

**Important:** Always provide both `upgrade()` and `downgrade()` functions for reversibility.

### Adding a New API Endpoint

1. Create route in `backend/app/api/{module}.py`:
```python
@router.post("/endpoint")
async def endpoint_name(
    data: SchemaIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> SchemaOut:
    # Implementation
```

2. Add schemas in `backend/app/schemas/{module}.py`
3. Include router in `backend/app/main.py`: `app.include_router(router, prefix="/api", tags=["module"])`
4. Add tests in `backend/tests/test_api/test_{module}.py`

## Deployment Notes

**Backend:**
- Use `gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker` for production
- Run Celery workers separately: `celery -A app.tasks.celery_app worker --concurrency=4`
- Ensure `DATABASE_URL` points to production database (Supabase hosted)
- Set `SECRET_KEY` to secure random value: `openssl rand -hex 32`

**Frontend:**
- Build with `npm run build` → outputs to `dist/`
- Deploy `dist/` to Vercel/Netlify/Cloudflare Pages
- Set `VITE_API_BASE_URL` to production backend URL

## Debugging Tips

**LangGraph Workflows:**
- Enable LangSmith tracing: `LANGCHAIN_TRACING_V2=true`
- View traces at smith.langchain.com
- Check `work_orders.execution_log` JSONB for state transitions
- Use `logger.info()` in node functions to track flow

**Agent Issues:**
- Check `agent_outputs.reasoning_trace` for LLM thought process
- Validate tool calls in intermediate steps
- Review confidence scores (low = needs review)
- Ensure policy constraints are passed correctly

**Database Issues:**
- Check migration status: `./migrate.sh current`
- View migration history: `./migrate.sh history`
- Enable SQL logging: Set `echo=True` in `create_engine()`

**WebSocket Disconnections:**
- Implement heartbeat ping every 30 seconds
- Handle reconnection logic in frontend
- Check Redis connection for session storage

## Documentation References

- **Architecture Deep-Dive:** `docs/architecture.md` (2,400+ lines, comprehensive technical design)
- **Quick Setup:** `SETUP.md` (20-minute setup guide)
- **Project Summary:** `PROJECT_SUMMARY.md` (high-level overview)
- **Database Schema:** `docs/database-schema.md`
- **API Examples:** `docs/api-examples.md`

## Success Criteria (SLOs)

**Technical:**
- Ingestion latency: ≤10 min per 100MB file
- Mapping reuse: ≥90% after first cycle
- Bank reconciliation: T+1 coverage ≥99%
- Duplicate detection: ≥95% precision, ≥85% recall
- Control logging: 100% actions logged

**Agent Performance:**
- Cash forecast MAPE: ≤10% @ 2-week horizon
- Revenue forecast MAPE: ≤8% @ 90-day horizon
- Margin bridge: ≥95% of GM delta explained
- Auto-rec clearance: ≥80% of reconciliations

**User Experience:**
- Upload-to-insight: ≤30 min median
- Exception resolution: ≤24 hrs P50
