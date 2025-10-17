# Agentic CFO Platform - Project Summary

**Version:** 0.2 (Excel-First Mode)
**Status:** Architecture & Design Phase
**Stack:** FastAPI + React + LangGraph + OpenRouter

---

## 📊 Project Overview

The **Agentic CFO Platform** is a multi-agent financial automation system that transforms Excel/CSV uploads into actionable insights via specialized AI agents orchestrated by LangGraph. It delivers cash forecasting, margin analysis, rolling forecasts, capital allocation, and embedded controls—all without requiring system integrations.

### Vision Statement

*"A CFO that never sleeps"* — Upload the Excel files you already export from your ERP/bank/POS systems, and let 30+ specialized agents deliver:
- 13-week cash forecasts with liquidity warnings
- Day-3 month-end close with auto-reconciliations
- Margin bridges (Price/Volume/Mix decomposition)
- Rolling forecasts and capital allocation rankings (EVA/NPV/IRR)
- Policy-as-code enforcement with immutable audit trails

---

## 🎯 Core Capabilities

### 1. File Intake Gateway
- **Multi-channel ingestion:** Web upload, SFTP drop box, email inbox
- **Template catalog:** TrialBalance, AP/AR OpenItems, POS_Sales, Production_Volumes, etc.
- **Mapping Studio:** Learns column mappings with semantic matching (ChromaDB)
- **Workbook Auditor:** Scans for macros, external links, hidden sheets, volatile formulas
- **Dataset versioning:** Full lineage tracking for every upload

### 2. LangGraph Orchestration
- **Work Order Graph:** Routes files through agent networks
- **State persistence:** PostgreSQL checkpointing for resumable workflows
- **Human-above-the-loop:** Approval gates at defined checkpoints
- **Real-time updates:** WebSocket progress tracking
- **Policy enforcement:** Guardrail and Critic agents validate all outputs

### 3. Agent Network (30+ Specialized Agents)

#### Treasury & Working Capital
- **Cash Commander:** 13-week forecasts, Monte Carlo confidence intervals, covenant checks
- **Receivables Radar:** DSO optimization, collection risk scoring
- **Payables Protector:** Duplicate detection (≥95% precision), early-pay ROI, terms optimization
- **Covenant Keeper:** Debt compliance, headroom monitoring

#### Record-to-Report & Performance
- **Close Copilot:** Auto-reconciliations (bank-to-GL, AR/AP subledger-to-control), accrual proposals
- **Margin Mechanic:** P/V/M bridges, inflation vs. productivity decomposition
- **Cost Genome:** Vendor taxonomy, consolidation opportunities

#### FP&A & Capital Allocation
- **Forecast Factory:** Rolling forecasts, scenario trees, variance explanations
- **Portfolio Allocator:** EVA/NPV/IRR ranking, risk-adjusted screens, capital envelope optimization
- **Deal Diligence:** M&A valuation triangulation, integration risk assessment

#### Controls & Compliance
- **Guardrail:** Policy enforcement (SoD, materiality, treasury limits, disclosure gates)
- **Critic:** Statistical validation, outlier detection, reconciliation verification
- **Compliance Scribe:** Audit log compilation, evidence bundle generation (ZIP exports)
- **Workbook Auditor:** Spreadsheet risk assessment

#### Industry-Specific Agents
- **Retail:** GMROI Optimizer, Promo ROI, Assortment, Store & Labor
- **Energy:** CFaR Analyst, Hedge Strategist, Turnaround Planner, Real-Options Capital, Emissions Accountant

### 4. Outputs & Artifacts
- **Excel:** Cash_Ladder.xlsx, GM_Bridge_BU_SKU.xlsx, Portfolio_Ranked.xlsx, Forecast_Rolling.xlsx
- **PDF:** Liquidity_Warnings.pdf, Covenant_Report.pdf
- **Word:** Investment_Memos.docx (auto-generated)
- **Evidence:** Audit_Binder.zip (artifacts + logs + policy versions)

---

## 🏗️ Architecture Highlights

### Stack Summary
**Backend:**
- **Orchestration:** LangGraph 0.2+ (agent workflows), LangChain 0.3+ (agent tooling)
- **LLMs:** OpenRouter API → GPT-4 Turbo (complex reasoning), Claude-3.5 Sonnet (data analysis), GPT-3.5 Turbo (routine tasks), Llama-3.1 70B (cost optimization)
- **Data:** Pandas 2.1+, Polars 0.20+, OpenPyXL 3.1+
- **Database:** PostgreSQL 15+ / Supabase, Redis 7.0+ (Celery broker + caching)
- **Task Queue:** Celery 5.3+ (async agent execution)
- **Vector Store:** ChromaDB 0.4+ (mapping memory)
- **Web:** FastAPI 0.109+, Uvicorn, WebSockets
- **Auth:** JWT (python-jose), bcrypt 4.1+

**Frontend:**
- **Core:** React 18+, TypeScript 5.3+, Vite 5+
- **UI:** Tailwind CSS 3.4+, Headless UI
- **State:** React Context, React Query (optional)
- **API:** Axios 1.6+, Native WebSocket API
- **Testing:** Jest 29+, React Testing Library

**Infrastructure:**
- Supabase PostgreSQL (hosted)
- Redis (Celery + caching)
- Local filesystem → S3 (future)
- Railway/Render (backend), Vercel/Netlify (frontend)

### Key Architectural Decisions

1. **LangGraph over CrewAI/AutoGen:**
   - Graph-based workflows → perfect for Work Order routing
   - State persistence → PostgreSQL checkpointing for resumable workflows
   - Cyclic execution → Guardrail → Agent → Critic → Agent feedback loops
   - Human-in-loop → native interrupt mechanism for approval gates

2. **OpenRouter Multi-Model Strategy:**
   - GPT-4 Turbo: Portfolio Allocator, Deal Diligence, Cash Commander
   - Claude-3.5 Sonnet: Margin Mechanic, Cost Genome, Critic
   - GPT-3.5 Turbo: Close Copilot, Guardrail, Workbook Auditor
   - Llama-3.1 70B: Bulk processing, cost optimization

3. **Excel-First (No Mandatory Integrations):**
   - Template catalog with mapping memory (semantic matching via ChromaDB)
   - Dataset versioning with full lineage
   - Workbook Auditor for spreadsheet risk mitigation
   - DQ validation with cross-file reconciliations

4. **Policy-as-Code:**
   - `Policy_Pack.xlsx` parsed into Pydantic models
   - Guardrail agent enforces at graph checkpoints
   - Override mechanism with approval logging
   - Versioned policies with effective dates

5. **Immutable Audit Trail:**
   - Append-only audit events table (PostgreSQL)
   - Full dataset lineage (input → processing → output)
   - Approval history with timestamps + rationale
   - Evidence bundles for auditors (ZIP exports)

---

## 📂 Project Structure

```
AgenticCFO/
├── backend/                        # Python FastAPI Backend
│   ├── app/
│   │   ├── agents/                # 30+ Finance agents
│   │   │   ├── treasury/          # Cash Commander, Receivables Radar, Payables Protector
│   │   │   ├── r2r/               # Close Copilot, Margin Mechanic, Cost Genome
│   │   │   ├── fpa/               # Forecast Factory, Portfolio Allocator, Deal Diligence
│   │   │   ├── control/           # Guardrail, Critic, Compliance Scribe
│   │   │   └── industry/          # Retail (GMROI, Promo ROI), Energy (CFaR, Hedge)
│   │   ├── orchestration/         # LangGraph workflows
│   │   ├── intake/                # File ingestion, Template Catalog, Mapping Studio
│   │   ├── data_quality/          # DQ validators, reconcilers
│   │   ├── policy/                # Policy engine
│   │   ├── artifacts/             # Output generation (Excel/PDF/Word)
│   │   ├── api/                   # FastAPI endpoints
│   │   ├── core/                  # Config, security
│   │   ├── models/                # SQLAlchemy models
│   │   └── tasks/                 # Celery tasks
│   └── tests/                     # Backend tests (70%+ coverage target)
│
├── frontend/                      # React TypeScript Frontend
│   ├── src/
│   │   ├── components/            # Upload Wizard, Mapping Studio, CFO Dashboard, Work Orders
│   │   ├── pages/                 # Login, Dashboard, Profile, Settings
│   │   ├── services/              # API services (auth, upload, work orders, artifacts)
│   │   ├── hooks/                 # useAuth, useWorkOrderUpdates (WebSocket)
│   │   └── context/               # AuthContext, WorkOrderContext
│   └── tests/                     # Frontend tests (70%+ coverage target)
│
├── docs/                          # Comprehensive documentation
│   ├── architecture.md            # 2,400+ lines of detailed architecture
│   ├── database-schema.md         # Database design
│   └── api-examples.md            # API usage examples
│
├── README.md                      # Project overview (you are here)
├── PROJECT_SUMMARY.md             # This file
└── SETUP.md                       # Quick setup guide
```

---

## 🎓 Example End-to-End Workflows

### Workflow 1: Close-to-Forecast (Monthly)
**Inputs:** TrialBalance.xlsx, JE_Detail.csv, BankStatement.csv, AR/AP_OpenItems.xlsx
**Agents:** DQ → Close Copilot → Margin Mechanic → Forecast Factory → Guardrail → Critic → Compliance Scribe
**Outputs:** Close_Status.xlsx (Day-3 checklist), Auto_Recs.xlsx, GM_Bridge_BU_SKU.xlsx, Forecast_Rolling.xlsx, Audit_Binder.zip
**SLOs:** Day-3 close, ≥80% recs auto-cleared, ≥95% GM variance explained

### Workflow 2: Cash Control (Weekly)
**Inputs:** BankStatement_Week12.csv, AP/AR_OpenItems.xlsx, Payments_Executed.csv
**Agents:** DQ → Cash Commander → Receivables Radar → Payables Protector → Covenant Keeper → Guardrail → Critic
**Outputs:** Cash_Ladder.xlsx (13-week forecast), Liquidity_Warnings.pdf, Collections_Prioritized.xlsx, Duplicates_Flagged.xlsx
**SLOs:** T+1 bank rec ≥99%, duplicate detection ≥95% precision, cash MAPE ≤10% @ 2-week

### Workflow 3: Capital Allocation (Quarterly)
**Inputs:** Project_Cases.xlsx, WACC_Policy.xlsx, Capacity_Constraints.xlsx
**Agents:** DQ → Portfolio Allocator → Critic → Guardrail → Deal Diligence (if M&A) → Compliance Scribe
**Outputs:** Portfolio_Ranked.xlsx (EVA-ranked), Investment_Memos.docx, Sensitivity_Tornado.xlsx
**SLOs:** 100% projects policy-compliant, EVA/NPV/IRR + downside case

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

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- LangGraph + OpenRouter integration
- File Intake Gateway (Upload API, Workbook Auditor, Mapping Studio)
- Dataset Versioning (PostgreSQL schema)
- Celery + Redis task queue
- ChromaDB integration
- WebSocket server

### Phase 2: Core Agents (Weeks 5-8)
- Work Order Graph (LangGraph StateGraph)
- Policy Engine + Guardrail agent
- Critic agent
- 5 pilot agents: Cash Commander, Close Copilot, Margin Mechanic, Forecast Factory, Payables Protector
- Compliance Scribe
- Artifact generation system

### Phase 3: Workflows (Weeks 9-12)
- Close-to-Forecast workflow
- Cash Control workflow
- Human-approval gates
- Exception queue + routing
- Testing with sample data

### Phase 4: Industry Packs (Weeks 13-16)
- Retail pack (GMROI, Promo ROI, Assortment)
- Energy pack (CFaR, Hedge Strategist)
- Industry-specific templates
- Agent customization

### Phase 5: UI (Weeks 17-20)
- Upload Wizard frontend
- Mapping Studio UI
- Work Order dashboard
- CFO Portal (KPI packs)
- Exception queue interface
- Artifact viewer

### Phase 6: Launch (Weeks 21-24)
- Integration testing
- Pilot deployment (1 client)
- SLO validation
- Documentation
- Production launch

---

## 🔐 Security & Compliance

### Data Security
- **TLS 1.3** for all API traffic
- **At-rest encryption** (Supabase default)
- **JWT authentication** + bcrypt password hashing
- **Tenant isolation** (PostgreSQL row-level security)

### Audit & Compliance
- **Immutable audit log** (append-only table)
- **Full dataset lineage** (input → processing → output)
- **Approval history** (timestamps + rationale)
- **Policy version tracking** (effective dates)

### Spreadsheet Risk Mitigation
- **Workbook Auditor** scans all uploads:
  - Macros (stripped by default)
  - External links (flagged)
  - Hidden sheets (reported)
  - Volatile formulas (NOW(), RAND())
- High-risk workbooks **quarantined** from payment flows

### Policy-as-Code
- **Materiality thresholds** enforced by Guardrail
- **SoD violations** detected
- **Treasury limits** validated (min cash, max exposure)
- **Disclosure gates** applied per policy pack

---

## 🌟 Key Differentiators

1. **Excel-First, Not API-First**
   - Zero mandatory integrations
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
   - Manufacturing (coming soon)

---

## 🎯 Use Cases

This platform is perfect for:

- **CFO offices** automating financial analysis
- **Finance teams** needing fast close + rolling forecasts
- **Treasury departments** managing cash + covenants
- **FP&A analysts** running scenarios + capital allocation
- **Controllers** seeking audit-ready evidence
- **Retail finance** optimizing GMROI + promotions
- **Energy finance** managing hedge strategies + production economics

---

## 📚 Documentation

- **[README.md](README.md)** - Project overview + quick start
- **[docs/architecture.md](docs/architecture.md)** - Comprehensive architecture (2,400+ lines, highly recommended!)
- **[docs/database-schema.md](docs/database-schema.md)** - Database design
- **[docs/api-examples.md](docs/api-examples.md)** - API usage examples
- **[SETUP.md](SETUP.md)** - Quick 5-minute setup guide

---

## 📞 Contact & Support

- **GitHub:** [github.com/yourrepo/AgenticCFO](https://github.com/yourrepo/AgenticCFO)
- **Email:** support@agenticcfo.com
- **Docs:** [docs.agenticcfo.com](https://docs.agenticcfo.com)

---

**Built with care for CFOs who want insights, not integrations.** 📊
