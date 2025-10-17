# Next Steps - Agentic CFO Platform

**Last Updated:** 2025-10-17

## Current Status

✅ **Completed:** File Intake Layer (Layer 1) with P0 and P1 fixes
- Security hardening (path traversal, file size validation, transaction management)
- Comprehensive audit trail (100% action logging)
- Granular error handling (proper HTTP status codes)
- Database optimization (composite indexes)

## Immediate Next Steps

### 1. Testing & Validation
**Priority:** High
**Estimated Time:** 2-4 hours

- [ ] Create sample test files (Excel/CSV) for each template type:
  - BankStatement.xlsx
  - TrialBalance.xlsx
  - AP_OpenItems.xlsx
  - AR_Aging.xlsx
  - POS_Sales.csv
- [ ] Test file upload API endpoint with samples
- [ ] Verify template detection accuracy
- [ ] Verify column mapping results
- [ ] Verify DQ validation checks
- [ ] Test error handling with malformed files
- [ ] Run `/tester-review` to analyze test coverage and generate missing test implementations

### 2. Layer 2: LangGraph Orchestration
**Priority:** High
**Estimated Time:** 4-6 days (MVP Sprint Days 6-8)

- [ ] Create Work Order State Graph schema
  - Define `WorkOrderState` TypedDict
  - Implement PostgreSQL checkpointing
  - Create state management utilities
- [ ] Implement graph nodes:
  - `dq_validation_node` (entry point)
  - `routing_node` (routes to appropriate agents)
  - `guardrail_node` (policy enforcement)
  - `critic_node` (quality review)
  - `approval_gate_node` (human-in-loop)
  - `artifact_generation_node` (output creation)
- [ ] Set up LangGraph execution flow:
  - Conditional edges based on Work Order objective
  - State persistence to PostgreSQL
  - Interrupt mechanism for approval gates
- [ ] Integration with file intake layer
  - Trigger Work Order on successful dataset creation
  - Pass dataset IDs and metadata to graph

### 3. Base Agent Architecture
**Priority:** High
**Estimated Time:** 1-2 days

- [ ] Create `backend/app/agents/base.py`:
  - `BaseFinanceAgent` abstract class
  - OpenRouter LLM integration
  - Tool execution framework
  - Output schema (reasoning_trace, confidence_score, artifacts)
- [ ] Create agent registry (`backend/app/agents/__init__.py`)
- [ ] Define agent configuration (`backend/app/orchestration/config.py`):
  - `AGENT_MODEL_MAP` (which model per agent)
  - Temperature and token limits
  - Retry policies

### 4. Cash Commander Agent (MVP)
**Priority:** High
**Estimated Time:** 3-4 days (MVP Sprint Days 6-8)

- [ ] Implement `backend/app/agents/treasury/cash_commander.py`
- [ ] Create custom tools:
  - `analyze_bank_statement` - Extract cash positions
  - `forecast_cash_flow` - Project future balances
  - `identify_outliers` - Flag unusual transactions
- [ ] Define system prompt and responsibilities
- [ ] Implement artifact generation:
  - `Cash_Ladder.xlsx` - 13-week rolling forecast
  - `Liquidity_Warnings.pdf` - Risk alerts
- [ ] Integration with LangGraph orchestration

### 5. Excel Artifact Generator
**Priority:** High
**Estimated Time:** 2-3 days (MVP Sprint Days 11-12)

- [ ] Create `backend/app/artifacts/excel_generator.py`
  - Template-based generation using openpyxl
  - Dynamic table creation
  - Chart generation (cash waterfall, variance bridge)
- [ ] Create artifact templates:
  - Cash Ladder template
  - GM Bridge template
  - Portfolio Ranking template
- [ ] File storage and checksum calculation

### 6. Frontend Components (MVP)
**Priority:** Medium
**Estimated Time:** 3-4 days (MVP Sprint Days 13-14)

- [ ] File upload component with drag-and-drop
- [ ] Work Order dashboard (real-time status)
- [ ] Dataset viewer with DQ results
- [ ] Artifact download/preview
- [ ] WebSocket integration for live updates

## Future Phases (Post-MVP)

### Phase 2: Additional Agents (Weeks 3-8)
- Close Copilot (R2R agent)
- Margin Mechanic (R2R agent)
- Receivables Radar (Treasury agent)
- Payables Protector (Treasury agent)
- Covenant Keeper (Treasury agent)
- Forecast Factory (FP&A agent)
- Portfolio Allocator (FP&A agent)

### Phase 3: Advanced Features (Weeks 9-16)
- ChromaDB semantic column mapping
- Workbook Auditor agent (macro detection, risk scoring)
- Mapping Studio UI
- Policy Pack editor
- Multi-channel ingestion (SFTP, email)

### Phase 4: Industry-Specific Agents (Weeks 17-20)
- Retail: GMROI Calculator, Promo ROI Analyzer
- Energy: CFaR Calculator, Hedge Optimizer
- Healthcare: Payor Mix Analyzer, Charge Capture

### Phase 5: Production Hardening (Weeks 21-22)
- Load testing and optimization
- Security audit
- Deployment automation
- Monitoring and alerting

### Phase 6: Launch (Weeks 23-24)
- Documentation finalization
- User training materials
- Beta user onboarding
- Production deployment

## Key Architecture References

- **Full Architecture:** [docs/architecture.md](docs/architecture.md)
- **Database Schema:** [docs/database-schema.md](docs/database-schema.md)
- **Project Instructions:** [CLAUDE.md](CLAUDE.md)
- **Setup Guide:** [SETUP.md](SETUP.md)
- **Progress Tracking:** [PROGRESS.md](PROGRESS.md)

## Development Workflow Reminder

When implementing new features, use this workflow:
1. Implement feature → 2. Run `/architect-review` → 3. Fix issues → 4. Run `/tester-review` → 5. Implement tests → 6. Commit

## Environment Variables Required

Before starting Layer 2, ensure these are set in `backend/.env`:
```env
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
REDIS_URL=redis://localhost:6379/0
CHROMA_PERSIST_DIRECTORY=/var/agenticcfo/chroma
LANGCHAIN_TRACING_V2=true  # Optional for debugging
LANGCHAIN_API_KEY=your-langsmith-key  # Optional
```

## Testing Strategy

**Backend Test Coverage Target:** 70%+
- Unit tests: Agent logic, tool functions, validators
- Integration tests: API endpoints, database operations, LangGraph workflows
- Agent tests: Mock LLM responses, verify tool calls, validate output schemas

**Frontend Test Coverage Target:** 70%+
- Component tests: React Testing Library
- Integration tests: User flows (login, upload, view work orders)
- E2E tests: (Future) Playwright for full workflows
