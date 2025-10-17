# MVP Roadmap - Quick Reference

**Timeline:** 2 weeks
**Goal:** Working demo with Cash Commander agent analyzing bank statements

---

## Week 1: Foundation

### Days 1-2: File Upload Infrastructure
- ✅ Database models (DONE)
- ✅ Database migrations (DONE)
- [ ] Upload API endpoint (`POST /api/intake/upload`)
- [ ] File storage (local filesystem)
- [ ] SHA-256 hash generation
- [ ] Basic file validation

**Success:** Can upload Excel file via API, file stored, record in DB

### Days 3-4: Template Detection & Mapping
- [ ] Simple keyword-based template detector (BankStatement)
- [ ] Hardcoded column mapper (Date, Description, Debit, Credit, Balance)
- [ ] Excel/CSV parser
- [ ] Dataset creation

**Success:** Uploaded file is parsed, columns mapped, Dataset record created

### Day 5: Data Quality Validation
- [ ] Required column checker
- [ ] Date format validator
- [ ] Numeric column validator
- [ ] Duplicate detector

**Success:** File validated, DQ results stored, errors reported

---

## Week 2: Agent & Output

### Days 6-8: Cash Commander Agent
- [ ] BaseFinanceAgent abstract class
- [ ] OpenRouter LLM client
- [ ] Cash Commander implementation
  - Bank statement analyzer
  - Cash burn calculator
  - 13-week forecast generator
- [ ] Custom tools (analyze_bank_statement, calculate_forecast)

**Success:** Agent processes dataset, returns structured output with forecast

### Days 9-10: LangGraph Orchestration
- [ ] Simple Work Order StateGraph
- [ ] State management (in-memory)
- [ ] Work Order CRUD operations
- [ ] Sync execution (no Celery yet)

**Success:** Upload → Agent → Output flows through LangGraph

### Days 11-12: Excel Output
- [ ] Excel generator using openpyxl
- [ ] Cash Ladder template (3 sheets)
- [ ] Artifact storage
- [ ] Download endpoint

**Success:** Cash_Ladder.xlsx generated with forecast data

### Days 13-14: Frontend & Testing
- [ ] Upload page (drag-and-drop)
- [ ] Results page (display output, download button)
- [ ] Simple dashboard
- [ ] End-to-end integration test
- [ ] Demo script

**Success:** Full demo flow works end-to-end through web UI

---

## MVP Demo Flow

1. **Open web UI** → Navigate to upload page
2. **Upload file** → `bank_statement_sample.xlsx`
3. **Processing** → Show status indicator (~1-2 min)
4. **View results** → Agent output summary displayed
   - Total cash position: $X.X million
   - Average daily burn: $XX,XXX
   - Runway: XX weeks
   - Confidence: XX%
5. **Download artifact** → `Cash_Ladder.xlsx`
6. **Review Excel** → 13-week forecast with reasoning

---

## Files to Create (MVP)

### Backend Structure
```
backend/app/
├── intake/
│   ├── __init__.py
│   ├── upload_api.py          # NEW
│   ├── template_detector.py   # NEW
│   ├── column_mapper.py        # NEW
│   └── dq_validator.py         # NEW
├── orchestration/
│   ├── __init__.py
│   ├── work_order_graph.py     # NEW
│   └── nodes.py                # NEW
├── agents/
│   ├── __init__.py
│   ├── base_agent.py           # NEW
│   └── treasury/
│       ├── __init__.py
│       └── cash_commander.py   # NEW
├── tools/
│   ├── __init__.py
│   └── cash_tools.py           # NEW
├── artifacts/
│   ├── __init__.py
│   └── excel_generator.py      # NEW
├── services/
│   ├── __init__.py
│   ├── file_service.py         # NEW
│   ├── work_order_service.py   # NEW
│   └── artifact_service.py     # NEW
├── core/
│   ├── llm_client.py           # NEW
│   └── file_storage.py         # NEW
└── schemas/
    ├── dataset.py              # NEW
    ├── work_order.py           # NEW
    └── artifact.py             # NEW
```

### Frontend Structure
```
frontend/src/
├── pages/
│   ├── UploadPage.tsx          # NEW
│   ├── ResultsPage.tsx         # NEW
│   └── DashboardPage.tsx       # NEW
├── components/
│   ├── FileUploader.tsx        # NEW
│   ├── WorkOrderStatus.tsx     # NEW
│   └── ForecastSummary.tsx     # NEW
└── services/
    └── api.ts                   # NEW (enhance existing)
```

---

## Dependencies to Add

### Backend
```bash
pip install langgraph langchain langchain-openai
pip install openpyxl  # Excel generation
pip install python-multipart  # File upload
pip install aiofiles  # Async file handling
```

### Frontend
```bash
npm install @tanstack/react-query
npm install react-dropzone  # File upload
npm install recharts  # Charts (optional)
```

---

## Environment Variables (MVP)

```env
# .env (backend)
DATABASE_URL=postgresql://user:password@localhost:5432/agenticcfo
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY
OPENROUTER_DEFAULT_MODEL=openai/gpt-4-turbo
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
UPLOAD_DIR=/tmp/agenticcfo/uploads
ARTIFACTS_DIR=/tmp/agenticcfo/artifacts
```

```env
# .env (frontend)
VITE_API_BASE_URL=http://localhost:8000
```

---

## Testing Checklist

### Unit Tests
- [ ] `test_upload_api.py` - File upload endpoint
- [ ] `test_template_detector.py` - Template detection
- [ ] `test_column_mapper.py` - Column mapping
- [ ] `test_dq_validator.py` - Data quality validation
- [ ] `test_cash_commander.py` - Agent logic (mocked LLM)
- [ ] `test_excel_generator.py` - Excel generation

### Integration Tests
- [ ] `test_mvp_flow.py` - End-to-end flow

### Manual Testing
- [ ] Upload various bank statement formats
- [ ] Test with malformed files
- [ ] Verify Excel output quality
- [ ] Check error handling

---

## Sample Data

Create `backend/sample_data/bank_statement_sample.xlsx`:

| Date       | Description          | Debit   | Credit  | Balance   |
|------------|---------------------|---------|---------|-----------|
| 2025-01-01 | Opening Balance     |         |         | 1,000,000 |
| 2025-01-02 | Payroll Payment     | 250,000 |         | 750,000   |
| 2025-01-05 | Customer Payment    |         | 150,000 | 900,000   |
| 2025-01-10 | Vendor Payment      | 80,000  |         | 820,000   |
| ...        | ...                 | ...     | ...     | ...       |

(50-100 rows covering 3-6 months)

---

## Demo Script Outline

### Setup (5 min)
1. Start backend: `./run.sh`
2. Open frontend: http://localhost:5173
3. Have sample file ready

### Demo (10 min)
1. **Intro** (2 min)
   - "This is the Agentic CFO Platform MVP"
   - "We'll upload a bank statement and get a 13-week cash forecast"

2. **Upload** (1 min)
   - Drag-and-drop bank_statement_sample.xlsx
   - Show validation and upload progress

3. **Processing** (2 min)
   - Show "Processing..." status
   - Explain what's happening:
     - Template detection
     - Column mapping
     - DQ validation
     - Cash Commander agent analysis

4. **Results** (3 min)
   - Show agent output summary
   - Highlight key insights (cash position, burn rate, runway)
   - Show confidence score and reasoning

5. **Artifact** (2 min)
   - Download Cash_Ladder.xlsx
   - Open in Excel
   - Walk through 3 sheets:
     - Summary
     - 13-Week Forecast
     - Assumptions & Reasoning

### Q&A (5 min)
- Answer questions
- Discuss next steps (full build)
- Gather feedback

---

## Next Steps After MVP

1. **Stakeholder feedback session**
   - Schedule within 1 week of demo
   - Gather requirements for full build
   - Prioritize agents

2. **Transition to production**
   - Code cleanup and refactoring
   - Add comprehensive tests
   - Security audit

3. **Begin full build**
   - Start Sprint 1 (Layer 1 enhancements)
   - Set up CI/CD pipeline
   - Plan agent implementation order

---

**Status:** 📋 Planning Complete - Ready to Code!
**Start Date:** [TBD]
**Demo Date:** [TBD - 2 weeks from start]
