# Agentic CFO Platform - Implementation Plan

**Version:** 1.0
**Last Updated:** October 16, 2025
**Approach:** MVP-First, then Full System Buildout
**Timeline:** 2-4 weeks for MVP, 12-20 weeks for full system

---

## Executive Summary

This document outlines the implementation strategy for the Agentic CFO Platform, a multi-agent financial automation system. We will follow a **two-phase approach**:

1. **Phase 1 (MVP)**: Build a working end-to-end demo with 1-2 agents to showcase capabilities to stakeholders
2. **Phase 2 (Full Build)**: Systematically implement all 5 layers and 30+ agents over the following weeks

---

## Phase 1: MVP Demo (Week 1-2)

### Goal
Create a working demonstration that shows:
- File upload (Bank Statement Excel/CSV)
- Basic template detection and column mapping
- **Cash Commander agent** analyzing the data
- Simple 13-week cash forecast output (Excel)
- Basic web UI to trigger and view results

### MVP Components

#### 1. Minimal File Intake (3-4 days)
**Location:** `backend/app/intake/`

- **Upload API** (`/api/intake/upload`)
  - Accept Excel/CSV files via multipart/form-data
  - Generate SHA-256 hash for deduplication
  - Store file to local filesystem or S3
  - Create `FileUpload` and `Dataset` records
  - Status: Simplified validation (file size, extension only)

- **Basic Template Detection**
  - Detect "BankStatement" template type by header keywords
  - Simple keyword matching: ["Date", "Description", "Debit", "Credit", "Balance"]

- **Hardcoded Column Mapping**
  - Map common bank statement columns to standardized schema
  - No ML/semantic search yet (ChromaDB deferred to Phase 2)
  - Store mapping in `MappingConfig` table

- **Basic DQ Validation**
  - Check for required columns
  - Validate date formats
  - Ensure numeric columns are parseable
  - Flag duplicates by date+amount

**Deliverables:**
- `app/intake/upload_api.py` - FastAPI upload endpoint
- `app/intake/template_detector.py` - Simple template detection
- `app/intake/column_mapper.py` - Hardcoded mapping logic
- `app/intake/dq_validator.py` - Basic validation rules
- `app/services/file_service.py` - Business logic layer

#### 2. Simplified LangGraph Orchestration (2-3 days)
**Location:** `backend/app/orchestration/`

- **Basic Work Order Flow**
  ```
  START → DQ Validation → Cash Commander → Artifact Generation → END
  ```
  - No guardrails or critic yet
  - No approval gates
  - Synchronous execution (no Celery yet)

- **State Management**
  - Simple in-memory state (PostgreSQL checkpointing deferred)
  - Minimal state: `{input_datasets, agent_outputs, status}`

**Deliverables:**
- `app/orchestration/work_order_graph.py` - LangGraph StateGraph
- `app/orchestration/nodes.py` - Node functions (validation, agent execution, artifact gen)
- `app/services/work_order_service.py` - CRUD operations

#### 3. Cash Commander Agent (3-4 days)
**Location:** `backend/app/agents/treasury/`

- **Capabilities**
  - Analyze bank statement data
  - Identify upcoming disbursements (recurring payments)
  - Calculate average daily cash burn
  - Generate simple 13-week cash forecast
  - Output confidence score

- **LLM Integration**
  - Use OpenRouter with GPT-4 Turbo
  - Single API call pattern (no complex tool chains yet)

- **Tools**
  - `analyze_bank_statement` - Parse transactions, categorize cash flows
  - `calculate_forecast` - Simple extrapolation based on historical patterns

**Deliverables:**
- `app/agents/base_agent.py` - BaseFinanceAgent abstract class
- `app/agents/treasury/cash_commander.py` - Cash Commander implementation
- `app/tools/cash_tools.py` - Custom tools for cash analysis
- `app/core/llm_client.py` - OpenRouter client wrapper

#### 4. Simple Excel Output (1-2 days)
**Location:** `backend/app/artifacts/`

- **Cash Ladder Excel File**
  - Sheet 1: Summary (total cash, burn rate, runway)
  - Sheet 2: 13-Week Forecast (week-by-week projections)
  - Sheet 3: Assumptions (agent reasoning, confidence score)
  - Basic formatting (no charts yet)

**Deliverables:**
- `app/artifacts/excel_generator.py` - Excel generation using openpyxl
- `app/services/artifact_service.py` - Artifact CRUD operations

#### 5. Minimal Frontend (2-3 days)
**Location:** `frontend/src/`

- **Upload Page**
  - Drag-and-drop file upload
  - File validation (client-side)
  - Upload progress indicator

- **Results Page**
  - Display work order status
  - Show agent output summary
  - Download artifact button

- **Simple Dashboard**
  - List recent uploads
  - Show work order history

**Deliverables:**
- `frontend/src/pages/UploadPage.tsx` - File upload UI
- `frontend/src/pages/ResultsPage.tsx` - Results display
- `frontend/src/pages/DashboardPage.tsx` - Simple dashboard
- `frontend/src/services/api.ts` - API client

#### 6. MVP Testing & Documentation (1-2 days)

- **Tests**
  - Unit tests for upload API
  - Integration test for end-to-end flow
  - Mock LLM responses for deterministic testing

- **Documentation**
  - MVP demo script
  - API documentation (Swagger/Redoc)
  - Setup instructions for demo environment

**Deliverables:**
- `tests/test_mvp_flow.py` - End-to-end integration test
- `docs/mvp-demo-script.md` - Demo walkthrough
- `docs/api-docs.md` - API documentation

### MVP Success Criteria

✅ **Must Have:**
1. Upload a bank statement Excel file via web UI
2. System automatically detects template type
3. Cash Commander agent analyzes the data
4. Generate 13-week cash forecast Excel output
5. Download and view the forecast
6. Complete flow takes <2 minutes (no async yet)

✅ **Demo Flow:**
1. Open web UI → Upload `bank_statement_sample.xlsx`
2. Show "Processing..." indicator
3. Display agent output summary (cash position, burn rate, runway)
4. Download `Cash_Ladder.xlsx` artifact
5. Show Excel with forecast and reasoning

---

## Phase 2: Full System Buildout (Week 3-20)

### Overview
After MVP validation with stakeholders, systematically build out all 5 layers and 30+ agents following the original architecture plan.

### Sprint Breakdown

#### Sprint 1-2: Complete Layer 1 (Weeks 3-4)
**Goal:** Production-ready file intake with security and ML-powered mapping

**Tasks:**
- [ ] Implement Workbook Auditor agent (detect macros, hidden sheets, external links)
- [ ] Integrate virus scanning (ClamAV or cloud service)
- [ ] Build Mapping Studio with ChromaDB semantic search
- [ ] Create template catalog for 10+ file types
  - Trial Balance
  - AP Open Items
  - AR Aging
  - POS Sales
  - Inventory
  - Bank Statements (enhanced)
  - Payroll Register
  - Budget vs Actual
  - Invoice Register
  - Payment History
- [ ] Advanced DQ validators (cross-file reconciliation, statistical outliers)
- [ ] Dataset versioning and lineage tracking
- [ ] File storage abstraction (local → S3 migration path)

**Deliverables:**
- Comprehensive file intake system
- 90%+ mapping reuse rate after first cycle
- Risk scoring for uploaded files

#### Sprint 3-4: Complete Layer 2 (Weeks 5-6)
**Goal:** Production-grade LangGraph orchestration with approval gates

**Tasks:**
- [ ] Implement full Work Order StateGraph with all node types
- [ ] Add PostgreSQL checkpointing for resumable workflows
- [ ] Build Guardrail agent with policy enforcement
- [ ] Build Critic agent for statistical validation
- [ ] Implement approval gate interrupts
- [ ] Create routing logic for 30+ agents
- [ ] Add feedback loop (Guardrail → Agent → Critic → Agent)
- [ ] State persistence and recovery
- [ ] Integrate Celery + Redis for async execution
- [ ] WebSocket integration for real-time progress

**Deliverables:**
- Robust orchestration engine
- Human-above-the-loop approval workflow
- Async agent execution
- Real-time progress tracking

#### Sprint 5-8: Treasury & R2R Agents (Weeks 7-10)
**Goal:** Complete all Treasury and Record-to-Report agents

**Treasury Agents (4 agents):**
- [ ] Cash Commander (enhanced from MVP)
  - Multi-bank reconciliation
  - Cash forecasting with Monte Carlo simulation
  - Liquidity warning system
  - Covenant compliance tracking
- [ ] Receivables Radar
  - AR aging analysis
  - Collection prioritization
  - DSO tracking and forecasting
  - Bad debt prediction
- [ ] Payables Protector
  - AP optimization
  - Early payment discount analysis
  - DPO management
  - Vendor spend analysis
- [ ] Covenant Keeper
  - Debt covenant monitoring
  - Ratio calculations (Debt/EBITDA, Current Ratio, etc.)
  - Compliance reporting
  - Breach warnings

**R2R Agents (3 agents):**
- [ ] Close Copilot
  - Day-3 month-end close
  - Auto-reconciliations (bank, AR, AP, inventory)
  - Journal entry suggestions
  - Close task management
- [ ] Margin Mechanic
  - Gross margin bridge analysis
  - Variance decomposition (price, volume, mix, cost)
  - Product/SKU profitability
  - BU/channel margin analysis
- [ ] Cost Genome
  - OpEx categorization and analysis
  - Cost driver identification
  - Variance explanations
  - Cost reduction opportunities

**Deliverables:**
- 7 production-ready agents
- Comprehensive test coverage
- Agent-specific artifacts (Excel, PDF reports)

#### Sprint 9-12: FP&A & Control Agents (Weeks 11-14)
**Goal:** Complete all FP&A and Control agents

**FP&A Agents (3 agents):**
- [ ] Forecast Factory
  - Rolling 12-month forecasts (revenue, COGS, OpEx)
  - Driver-based modeling
  - Scenario planning (base, upside, downside)
  - Budget vs actual variance analysis
- [ ] Portfolio Allocator
  - Capital project ranking
  - NPV/IRR/payback analysis
  - Portfolio optimization
  - Investment memos
- [ ] Deal Diligence
  - M&A due diligence support
  - Quality of earnings analysis
  - Synergy identification
  - Integration planning

**Control Agents (4 agents):**
- [ ] Guardrail (enhanced from Sprint 3)
  - Materiality thresholds
  - Segregation of duties
  - Treasury limits
  - Disclosure gates
- [ ] Critic (enhanced from Sprint 3)
  - Statistical validation
  - Cross-check agent outputs
  - Confidence scoring
  - Quality assurance
- [ ] Compliance Scribe
  - Audit trail documentation
  - Control testing evidence
  - SOX compliance support
  - Regulatory reporting
- [ ] Workbook Auditor (enhanced from Sprint 1)
  - Deep Excel analysis
  - Formula auditing
  - Circular reference detection
  - Sensitivity analysis

**Deliverables:**
- 7 additional agents
- Policy-as-code enforcement
- Comprehensive audit trails

#### Sprint 13-14: Industry-Specific Agents (Weeks 15-16)
**Goal:** Add vertical-specific agents

**Retail Agents (2 agents):**
- [ ] GMROI Optimizer
  - Gross margin return on investment
  - Inventory turn analysis
  - Product lifecycle management
- [ ] Promo ROI Analyzer
  - Promotional effectiveness
  - Lift analysis
  - ROI calculations

**Energy Agents (2 agents):**
- [ ] CFaR (Cash Flow at Risk)
  - Commodity price risk
  - VaR calculations
  - Stress testing
- [ ] Hedge Optimizer
  - Hedging strategy recommendations
  - Collar analysis
  - Cost-benefit analysis

**SaaS Agents (2 agents):**
- [ ] CAC/LTV Tracker
  - Customer acquisition cost analysis
  - Lifetime value modeling
  - Unit economics
- [ ] Churn Prophet
  - Churn prediction
  - Cohort analysis
  - Revenue retention metrics

**Deliverables:**
- 6 industry-specific agents
- Vertical templates and mappings
- Industry benchmarks

#### Sprint 15-16: Layer 4 & 5 Completion (Weeks 17-18)
**Goal:** Production-grade tools and artifact generation

**Layer 4: LLM & Tool Layer**
- [ ] Custom Finance Tools
  - `calculate_npv` - NPV/IRR/payback
  - `calculate_wacc` - WACC calculator
  - `analyze_variance` - Statistical variance decomposition
  - `monte_carlo_simulation` - Monte Carlo forecasting
  - `ratio_calculator` - Financial ratios
  - `time_series_forecast` - Prophet/ARIMA forecasting
- [ ] ChromaDB Production Setup
  - Persistent storage
  - Collection management
  - Embedding strategies
  - Similarity search optimization
- [ ] OpenRouter Multi-Model Optimization
  - Model routing logic (GPT-4 vs Claude vs Llama)
  - Cost tracking per agent
  - Fallback mechanisms
  - Rate limit handling

**Layer 5: Output & Audit Layer**
- [ ] Excel Artifact Generator (production-grade)
  - Charts and visualizations
  - Conditional formatting
  - Data validation
  - Multiple sheet templates
- [ ] PDF Report Generator
  - Executive summaries
  - Compliance reports
  - Covenant reports
- [ ] Word Document Generator
  - Investment memos
  - Audit documentation
  - Policy documents
- [ ] Audit Trail System
  - Append-only logging
  - Lineage tracking
  - Integrity verification (checksums)
  - Compliance reporting

**Deliverables:**
- Comprehensive tool library
- Production artifact generation
- Full audit trail system

#### Sprint 17-18: Frontend Completion (Weeks 19-20)
**Goal:** Production-ready user interface

**Components:**
- [ ] Upload Wizard
  - Multi-file upload
  - Template selection
  - Mapping confirmation
  - Preview and validation
- [ ] Mapping Studio
  - Column mapping UI
  - Semantic suggestions from ChromaDB
  - Save and reuse mappings
  - Drift detection
- [ ] CFO Dashboard
  - KPI summary cards
  - Cash ladder visualization
  - Exception alerts
  - Work order status
- [ ] Work Order Detail Page
  - Progress tracking
  - Agent outputs
  - Approval workflow UI
  - Artifact downloads
- [ ] Policy Pack Editor
  - Visual policy configuration
  - Validation rules
  - Version management
- [ ] Admin Console
  - User management
  - Tenant settings
  - Agent configuration
  - System monitoring

**Deliverables:**
- Complete React frontend
- Production-ready UI/UX
- Mobile-responsive design

#### Sprint 19-20: Testing & Production Readiness (Week 21-22)
**Goal:** Comprehensive testing and deployment preparation

**Testing:**
- [ ] Unit tests (70%+ coverage)
  - All agents
  - All services
  - All API endpoints
- [ ] Integration tests
  - End-to-end workflows
  - Multi-agent orchestration
  - Approval gates
- [ ] Agent tests
  - Mock LLM responses
  - Tool call verification
  - Output schema validation
- [ ] Performance tests
  - File upload limits (100MB+)
  - Concurrent user load
  - Agent execution time
- [ ] Security tests
  - Authentication/authorization
  - SQL injection prevention
  - File upload vulnerabilities
  - API rate limiting

**Production Readiness:**
- [ ] Environment configuration
  - Production .env files
  - Secret management (AWS Secrets Manager)
  - Database connection pooling
- [ ] Deployment automation
  - Docker containerization
  - CI/CD pipeline (GitHub Actions)
  - Blue-green deployment
- [ ] Monitoring and observability
  - Application logs (CloudWatch)
  - LLM call tracking (LangSmith)
  - Error alerting (Sentry)
  - Performance metrics (DataDog)
- [ ] Documentation
  - User guide
  - API documentation
  - Admin guide
  - Troubleshooting guide

**Deliverables:**
- Production-ready system
- Comprehensive test suite
- Deployment automation
- Monitoring and alerting

---

## Technical Architecture Decisions

### MVP vs Full Build Tradeoffs

| Component | MVP Approach | Full Build Approach |
|-----------|--------------|---------------------|
| **File Upload** | Local filesystem | S3 with CloudFront CDN |
| **Column Mapping** | Hardcoded rules | ChromaDB semantic search |
| **Validation** | Basic checks | Cross-file reconciliation, ML anomaly detection |
| **Orchestration** | Synchronous, in-memory state | Celery async, PostgreSQL checkpointing |
| **Agents** | 1 agent (Cash Commander) | 30+ agents across 5 categories |
| **LLM** | Single model (GPT-4) | Multi-model routing with fallbacks |
| **Approval Gates** | None | Human-above-the-loop with interrupts |
| **Artifacts** | Simple Excel | Excel + PDF + Word with rich formatting |
| **Frontend** | Basic React pages | Full-featured SPA with real-time updates |
| **Testing** | Happy path only | Comprehensive unit + integration + E2E |
| **Deployment** | Local dev | Production AWS infrastructure |

### Technology Stack

**Backend:**
- FastAPI (Python 3.11+)
- LangGraph for orchestration
- OpenRouter for multi-model LLM access
- PostgreSQL 14+ with JSONB
- Redis for caching and Celery
- ChromaDB for semantic search
- SQLAlchemy 2.0 for ORM
- Alembic for migrations
- Celery for async tasks

**Frontend:**
- React 18+
- TypeScript
- Vite build tool
- TanStack Query for data fetching
- Zustand for state management
- shadcn/ui for components
- Recharts for visualizations

**Infrastructure:**
- AWS (S3, RDS, ElastiCache, Lambda)
- Docker + Docker Compose
- GitHub Actions for CI/CD
- Terraform for IaC (Phase 2)

**Observability:**
- LangSmith for LLM tracing
- Sentry for error tracking
- CloudWatch for logs
- DataDog for metrics (Phase 2)

### Environment Variables

**MVP Required:**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agenticcfo

# LLM
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
OPENROUTER_DEFAULT_MODEL=openai/gpt-4-turbo

# Application
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173

# Storage (MVP: local filesystem)
UPLOAD_DIR=/tmp/agenticcfo/uploads
ARTIFACTS_DIR=/tmp/agenticcfo/artifacts
```

**Full Build Additional:**
```env
# AWS
AWS_ACCESS_KEY_ID=YOUR_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET
S3_BUCKET=agenticcfo-uploads

# Redis
REDIS_URL=redis://localhost:6379/0

# ChromaDB
CHROMA_PERSIST_DIRECTORY=/var/agenticcfo/chroma
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Observability
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
SENTRY_DSN=your-sentry-dsn

# Email (for SFTP/email ingestion)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email
SMTP_PASSWORD=your-password
```

---

## Development Workflow

### MVP Development Process (Weeks 1-2)

**Daily Standup Questions:**
1. What did you complete yesterday?
2. What are you working on today?
3. Any blockers?

**Weekly Milestones:**
- **End of Week 1:** File upload + template detection + column mapping working
- **End of Week 2:** Cash Commander agent + Excel output + basic UI complete

**Code Review Process:**
1. Implement feature
2. Run `/architect-review` to check architectural alignment
3. Fix any issues
4. Run `/tester-review` to identify missing tests
5. Implement tests
6. Create PR for review
7. Merge after approval

### Full Build Development Process (Weeks 3-22)

**Sprint Cadence (2-week sprints):**
- Monday: Sprint planning
- Daily: Standup (15 min)
- Thursday: Mid-sprint check-in
- Friday: Sprint review + retrospective

**Definition of Done:**
- [ ] Code complete and merged
- [ ] Unit tests written (70%+ coverage)
- [ ] Integration tests written
- [ ] `/architect-review` passed
- [ ] `/tester-review` passed
- [ ] Documentation updated
- [ ] Deployed to dev environment

**Code Quality Gates:**
- Black for formatting
- Flake8 for linting
- MyPy for type checking
- Pytest for testing (70%+ coverage required)
- Pre-commit hooks for all checks

---

## Risk Management

### MVP Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| OpenRouter API downtime | High | Low | Add retry logic, mock responses for demo |
| LLM hallucinations | High | Medium | Add validation checks, show confidence scores |
| File parsing errors | Medium | Medium | Extensive validation, clear error messages |
| Slow agent execution | Medium | Medium | Set expectations (2-5 min processing time) |
| Scope creep | High | High | Strict MVP feature freeze, defer to Phase 2 |

### Full Build Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Agent complexity underestimated | High | Medium | Prototype agents early, adjust timeline |
| LangGraph learning curve | Medium | Medium | Allocate time for spikes and experimentation |
| Integration challenges | Medium | High | Build thin vertical slices, test early |
| Performance issues | High | Low | Load testing, optimization sprints |
| Security vulnerabilities | High | Medium | Regular security audits, penetration testing |

---

## Success Metrics

### MVP Success Criteria

**Technical:**
- [ ] Upload file → Download forecast in <2 minutes
- [ ] Cash Commander accuracy: MAPE ≤15% @ 2-week horizon (sample data)
- [ ] Zero critical bugs in demo
- [ ] System handles 10MB Excel files

**Business:**
- [ ] Positive stakeholder feedback on demo
- [ ] Secure funding/approval for full build
- [ ] 3+ potential customers interested

### Full Build Success Criteria (from architecture.md)

**Technical:**
- [ ] Ingestion latency: ≤10 min per 100MB file
- [ ] Mapping reuse: ≥90% after first cycle
- [ ] Bank reconciliation: T+1 coverage ≥99%
- [ ] Duplicate detection: ≥95% precision, ≥85% recall
- [ ] Control logging: 100% actions logged

**Agent Performance:**
- [ ] Cash forecast MAPE: ≤10% @ 2-week horizon
- [ ] Revenue forecast MAPE: ≤8% @ 90-day horizon
- [ ] Margin bridge: ≥95% of GM delta explained
- [ ] Auto-rec clearance: ≥80% of reconciliations

**User Experience:**
- [ ] Upload-to-insight: ≤30 min median
- [ ] Exception resolution: ≤24 hrs P50
- [ ] User satisfaction: 4.5/5 stars

---

## Next Steps

### Immediate Actions (This Week)

1. **Set up MVP development environment**
   - [ ] Clone sample bank statement data
   - [ ] Configure OpenRouter API key
   - [ ] Create MVP feature branch

2. **Start MVP Sprint 1**
   - [ ] Implement upload API endpoint
   - [ ] Build basic template detector
   - [ ] Create hardcoded column mapper
   - [ ] Set up DQ validator

3. **Weekly Check-in**
   - [ ] Review progress against MVP timeline
   - [ ] Adjust scope if needed
   - [ ] Prepare demo script draft

### After MVP Demo

1. **Gather stakeholder feedback**
   - What worked well?
   - What needs improvement?
   - Which agents are highest priority?

2. **Refine full build roadmap**
   - Adjust sprint priorities based on feedback
   - Update timeline estimates
   - Identify additional resources needed

3. **Begin Sprint 1 of full build**
   - Transition MVP code to production-ready
   - Start implementing Layer 1 enhancements

---

## Appendix

### Sample Data Requirements

**MVP:**
- Bank statement (Excel/CSV) with 3-6 months of transactions
- Minimum columns: Date, Description, Debit, Credit, Balance

**Full Build:**
- Trial Balance (10+ templates)
- AP Open Items
- AR Aging
- POS Sales data
- Inventory snapshots
- Payroll registers
- Budget vs Actual reports

### Reference Documentation

- [Architecture Deep-Dive](./architecture.md) - Comprehensive technical design
- [Database Schema](./database-schema.md) - Full schema documentation
- [API Examples](./api-examples.md) - API usage examples
- [CLAUDE.md](../CLAUDE.md) - Project instructions for Claude Code
- [MVP Demo Script](./mvp-demo-script.md) - To be created

### Key Contacts

- **Product Owner:** [TBD]
- **Tech Lead:** [TBD]
- **DevOps:** [TBD]
- **Stakeholders:** [TBD]

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-16 | Claude Code | Initial implementation plan created |

---

**Last Updated:** October 16, 2025
**Status:** 🚀 Ready to Begin MVP Development
