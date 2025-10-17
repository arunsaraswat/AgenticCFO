# Agentic CFO Platform - Architecture Documentation

**Version:** 0.2 (Excel-First Mode)
**Last Updated:** January 2025
**Status:** Design & Implementation Phase

---

## Executive Summary

The **Agentic CFO Platform** is a multi-agent financial automation system that processes Excel/CSV files to deliver five critical insight areas: cash management, margin truth, forecasting & capital allocation, growth/unit economics, and embedded controls. The platform operates as a "CFO that never sleeps" through a supervised mesh of specialized finance agents orchestrated by **LangGraph**.

### Core Vision

Ship a supervised agent network that consumes uploaded Excel/CSV files (no mandatory integrations) to deliver:
- 13-week cash forecasting with liquidity warnings
- Day-3 month-end close with auto-reconciliations
- Margin bridges and variance explanations
- Rolling forecasts and capital allocation rankings
- Policy-as-code enforcement with audit trails

### Key Architectural Principles

1. **Excel-First**: All insights run from uploaded files; zero required system integrations
2. **Policy-as-Code**: Guardrails enforce materiality, SoD, treasury limits, disclosure gates
3. **Explainable**: Every agent output includes reasoning traces, confidence scores, and artifacts
4. **Auditable**: Immutable logs, dataset lineage, approval workflows
5. **Human-Above-the-Loop**: Supervisors approve at defined gates; agents recommend, humans decide

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │Upload Wizard │  │Mapping Studio│  │CFO Dashboard │              │
│  │              │  │              │  │              │              │
│  │ • Drag-drop  │  │ • Column map │  │ • KPI packs  │              │
│  │ • Template   │  │ • Memory     │  │ • Cash ladder│              │
│  │   detection  │  │ • Drift      │  │ • Exceptions │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                  │                  │                       │
│         └──────────────────┴──────────────────┘                      │
│                            │                                          │
│                    REST API + WebSocket                              │
│                            │                                          │
└────────────────────────────┼──────────────────────────────────────────┘
                             │
┌────────────────────────────▼──────────────────────────────────────────┐
│                    BACKEND (FastAPI + Python)                         │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              LAYER 1: FILE INTAKE GATEWAY                     │   │
│  │                                                               │   │
│  │  Upload API ──┬─→ [Virus Scan] ──→ [Workbook Auditor]       │   │
│  │               │                                               │   │
│  │  SFTP Drop  ──┤                                               │   │
│  │               │                                               │   │
│  │  Email Inbox──┘   ↓                                          │   │
│  │                                                               │   │
│  │           [Template Catalog] → [Mapping Studio]              │   │
│  │                    ↓                                          │   │
│  │           [Data Quality Validator]                           │   │
│  │                    ↓                                          │   │
│  │           [Dataset Staging & Versioning]                     │   │
│  └───────────────────────┬───────────────────────────────────────┘   │
│                          │                                            │
│  ┌───────────────────────▼───────────────────────────────────────┐   │
│  │     LAYER 2: ORCHESTRATION (LangGraph StateGraph)            │   │
│  │                                                               │   │
│  │    START                                                      │   │
│  │      │                                                        │   │
│  │      ▼                                                        │   │
│  │  [DQ Validation] ──→ [Routing Logic]                         │   │
│  │      │                    │                                   │   │
│  │      │                    ├─→ Cash Commander                  │   │
│  │      │                    ├─→ Close Copilot                   │   │
│  │      │                    ├─→ Margin Mechanic                 │   │
│  │      │                    ├─→ Forecast Factory                │   │
│  │      │                    └─→ Portfolio Allocator             │   │
│  │      │                         │                              │   │
│  │      │                         ▼                              │   │
│  │      │                    [Guardrail] ──→ Policy Check        │   │
│  │      │                         │                              │   │
│  │      │                         ▼                              │   │
│  │      │                    [Critic] ──→ Statistical Validation │   │
│  │      │                         │                              │   │
│  │      │                         ▼                              │   │
│  │      │                [Approval Gate] ←─ Human Review         │   │
│  │      │                         │                              │   │
│  │      │                         ▼                              │   │
│  │      │                [Artifact Generation]                   │   │
│  │      │                         │                              │   │
│  │      └─────────────────────────▼                              │   │
│  │                             END                               │   │
│  │                                                               │   │
│  │  Policy Engine: Enforces materiality, SoD, limits, gates     │   │
│  └───────────────────────┬───────────────────────────────────────┘   │
│                          │                                            │
│  ┌───────────────────────▼───────────────────────────────────────┐   │
│  │         LAYER 3: AGENT NETWORK (30+ Specialized Agents)      │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │ TREASURY & WORKING CAPITAL                              │ │   │
│  │  │  • Cash Commander (13-week forecast, liquidity alerts) │ │   │
│  │  │  • Receivables Radar (DSO, collection prioritization)  │ │   │
│  │  │  • Payables Protector (duplicates, early-pay ROI)      │ │   │
│  │  │  • Covenant Keeper (debt compliance, headroom)         │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │ RECORD-TO-REPORT & PERFORMANCE                          │ │   │
│  │  │  • Close Copilot (auto-recs, accruals, Day-3 status)   │ │   │
│  │  │  • Margin Mechanic (P/V/M bridges, inflation analysis) │ │   │
│  │  │  • Cost Genome (vendor taxonomy, consolidation)        │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │ FP&A & CAPITAL ALLOCATION                               │ │   │
│  │  │  • Forecast Factory (rolling forecasts, scenarios)     │ │   │
│  │  │  • Portfolio Allocator (EVA/NPV/IRR ranking)           │ │   │
│  │  │  • Deal Diligence (M&A valuation, integration risks)   │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │ GROWTH & UNIT ECONOMICS                                 │ │   │
│  │  │  • Revenue Quality (cohort LTV, NRR/GRR)               │ │   │
│  │  │  • Promo ROI (Retail: keep/cut recommendations)        │ │   │
│  │  │  • GMROI Optimizer (Retail: assortment, markdown)      │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │ CONTROLS & COMPLIANCE                                   │ │   │
│  │  │  • Guardrail (policy enforcement, SoD checks)          │ │   │
│  │  │  • Critic (statistical validation, outlier detection)  │ │   │
│  │  │  • Compliance Scribe (audit logs, evidence bundles)    │ │   │
│  │  │  • Workbook Auditor (macro/link/formula risk checks)   │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │ INDUSTRY-SPECIFIC AGENTS                                │ │   │
│  │  │  Retail: GMROI, Promo ROI, Assortment, Store & Labor   │ │   │
│  │  │  Energy: CFaR Analyst, Hedge Strategist, Turnaround    │ │   │
│  │  │          Real-Options Capital, Emissions Accountant     │ │   │
│  │  └─────────────────────────────────────────────────────────┘ │   │
│  └───────────────────────┬───────────────────────────────────────┘   │
│                          │                                            │
│  ┌───────────────────────▼───────────────────────────────────────┐   │
│  │         LAYER 4: LLM & TOOL LAYER                            │   │
│  │                                                               │   │
│  │  OpenRouter Multi-Model Strategy:                            │   │
│  │  • GPT-4 Turbo (Complex reasoning, capital allocation)       │   │
│  │  • Claude-3.5 Sonnet (Data analysis, margin mechanics)       │   │
│  │  • GPT-3.5 Turbo (Routine tasks, DQ checks)                  │   │
│  │  • Llama-3.1 70B (Cost optimization for bulk processing)     │   │
│  │                                                               │   │
│  │  LangChain Tools:                                            │   │
│  │  • Pandas/Polars (Excel/CSV data processing)                 │   │
│  │  • OpenPyXL (Workbook manipulation, artifact generation)     │   │
│  │  • Custom Finance Tools (NPV, IRR, WACC, CFaR calculators)   │   │
│  │  • SQL Query Tools (dataset retrieval from PostgreSQL)       │   │
│  │                                                               │   │
│  │  ChromaDB (Vector Store):                                    │   │
│  │  • Mapping memory (semantic column matching)                 │   │
│  │  • Historical variance explanations                          │   │
│  │  • Similar transaction lookups                               │   │
│  └───────────────────────┬───────────────────────────────────────┘   │
│                          │                                            │
│  ┌───────────────────────▼───────────────────────────────────────┐   │
│  │         LAYER 5: OUTPUT & AUDIT LAYER                        │   │
│  │                                                               │   │
│  │  Artifact Generation:                                        │   │
│  │  • Cash_Ladder.xlsx, 13W_Forecast.xlsx                       │   │
│  │  • GM_Bridge_BU_SKU.xlsx, Margin_Waterfall.xlsx              │   │
│  │  • Forecast_Rolling.xlsx, Scenario_Compare.xlsx              │   │
│  │  • Portfolio_Ranked.xlsx, Investment_Memos.docx              │   │
│  │  • Liquidity_Warnings.pdf, Covenant_Report.pdf               │   │
│  │                                                               │   │
│  │  Artifact Storage: Local Filesystem → S3 (future)            │   │
│  │                                                               │   │
│  │  Audit Logs (PostgreSQL):                                    │   │
│  │  • Immutable event log (who, what, when, why)                │   │
│  │  • Dataset lineage (input → processing → output)             │   │
│  │  • Approval history (gate name, approver, decision)          │   │
│  │  • Policy violations (check name, severity, remediation)     │   │
│  │                                                               │   │
│  │  Evidence Bundles:                                           │   │
│  │  • ZIP exports with artifacts + logs + policy versions       │   │
│  │  • Disclosure checklists with supporting reconciliations     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

       ┌─────────────────────────────────────────────────┐
       │   INFRASTRUCTURE SERVICES                        │
       │                                                  │
       │  • PostgreSQL/Supabase (DB + Caching)           │
       │  • Redis (Celery task queue + session cache)    │
       │  • Celery (Async agent execution workers)       │
       │  • WebSocket Server (Real-time progress)        │
       │  • ChromaDB (Vector store for mapping memory)   │
       │  • Local Filesystem (Artifact storage)          │
       └─────────────────────────────────────────────────┘
```

---

## Layer 1: File Intake Gateway

### Responsibilities

1. **Multi-channel ingestion**: Web upload, SFTP drop box, email inbox
2. **Security scanning**: Virus detection, macro stripping, malicious content blocking
3. **Spreadsheet risk assessment**: External links, hidden sheets, volatile formulas
4. **Template detection**: Auto-identify file type (TrialBalance, AP_OpenItems, POS_Sales, etc.)
5. **Column mapping**: Match source columns to template schema using ML + memory
6. **Data quality validation**: Completeness, type checks, duplicates, reconciliations
7. **Dataset versioning**: Snapshot every upload with lineage tracking

### Components

#### Upload API (FastAPI)
```python
@router.post("/api/intake/upload")
async def upload_file(
    file: UploadFile,
    template_type: Optional[str] = None,
    tenant_id: str = Depends(get_current_tenant),
    current_user: User = Depends(get_current_user)
):
    """
    Upload Excel/CSV file for processing

    Workflow:
    1. Save file to temp storage
    2. Run virus scan (python-magic signature check)
    3. Execute Workbook Auditor agent
    4. Detect template type (if not provided)
    5. Apply mapping configuration (from mapping memory)
    6. Run DQ validation
    7. Stage dataset with version increment
    8. Create Work Order
    9. Return upload_id and work_order_id
    """
```

#### Workbook Auditor Agent
```python
class WorkbookAuditorAgent(BaseFinanceAgent):
    """
    Scans Excel files for spreadsheet risks:
    - Macros (VBA code)
    - External links (to other workbooks or URLs)
    - Hidden sheets (suspicious data hiding)
    - Volatile formulas (NOW(), RAND(), TODAY())
    - Protected ranges (locked cells)
    - Data validation issues

    Outputs: WorkbookRiskReport with severity (high/medium/low)
    """

    def get_system_prompt(self) -> str:
        return """You are the Workbook Auditor, responsible for identifying
        spreadsheet risks in uploaded Excel files. Analyze the workbook structure
        and flag any issues that could compromise data integrity or security.

        Check for:
        1. Macros or VBA code
        2. External links (other workbooks, websites)
        3. Hidden sheets or columns
        4. Volatile formulas that recalculate unpredictably
        5. Circular references
        6. Protected/locked cells without clear documentation

        Assign severity:
        - HIGH: Macros, external links to unknown sources
        - MEDIUM: Hidden sheets with data, many volatile formulas
        - LOW: Cosmetic issues, standard protections

        Recommend remediation actions."""
```

#### Mapping Studio

**Mapping Memory System:**
- **First Upload**: User confirms column mappings via UI
- **Subsequent Uploads**: Reuse mapping if columns match (exact or >90% similarity)
- **Drift Detection**: Alert if column names change, add/remove columns
- **Semantic Matching**: Use ChromaDB embeddings for fuzzy column matching

```python
# Example Mapping Configuration
{
    "mapping_id": "uuid-123",
    "tenant_id": "tenant-456",
    "template_type": "TrialBalance",
    "source_file_pattern": "*_TB_*.xlsx",
    "column_mappings": {
        "AcctNum": "AccountNumber",
        "Acct_Name": "AccountName",
        "Dept": "Department",
        "Period": "Period",
        "Amt": "Balance_FuncCurr"
    },
    "date_formats": {
        "Period": "%Y%m"
    },
    "currency_rules": {
        "default_currency": "USD",
        "currency_column": "Currency"
    },
    "created_at": "2025-01-15T10:30:00Z",
    "use_count": 15,
    "last_used_at": "2025-01-20T14:22:00Z"
}
```

#### Data Quality Validator

**Pre-Flight Checks:**
1. **Completeness**: Required columns present, no nulls in key fields
2. **Type Checks**: Dates are dates, numbers are numbers, amounts are numeric
3. **Duplicates**: Flag duplicate invoice numbers, transaction IDs
4. **Period Coverage**: Ensure all days/weeks covered (no gaps)
5. **Entity/Currency Sanity**: Consistent entity codes, valid ISO currency codes

**Cross-File Reconciliations:**
- Trial Balance: Debit - Credit = 0 (balanced)
- Bank-to-GL: Bank statement closing balance = GL cash account balance (±tolerance)
- AR/AP Subledger: Sum of open items = GL control account balance

**Output:** `DQ_Report.html` with pass/fail status, exception queue

---

## Layer 2: Orchestration with LangGraph

### Work Order Graph Architecture

Every file upload triggers a **Work Order** that flows through a **LangGraph StateGraph**.

#### StateGraph Design Pattern

```python
from typing import TypedDict, List, Optional, Literal
from datetime import datetime

class WorkOrderState(TypedDict):
    """
    State object that flows through the LangGraph.
    Immutable transitions ensure full audit trail.
    """

    # Work Order Metadata
    work_order_id: str
    tenant_id: str
    objective: str  # "Produce 13-week cash forecast"
    priority: Literal["high", "medium", "low"]
    created_at: datetime
    sla_deadline: datetime

    # Input Datasets
    input_datasets: List[dict]  # [{dataset_id, template_type, version, period}]

    # Policy References
    policy_refs: List[str]  # ["Policy_Pack_V3#Treasury", "Policy_Pack_V3#Materiality"]

    # Processing State
    current_stage: str  # "ingestion" | "dq" | "routing" | "agent_processing" | "guardrail" | "critic" | "approval" | "artifact_gen" | "completed"

    # Agent Outputs
    agent_outputs: dict  # {agent_name: {output, confidence, artifacts, execution_time, cost}}

    # Validation Results
    dq_results: Optional[dict]
    guardrail_checks: List[dict]  # [{check_name, status, reason, severity}]
    critic_validations: List[dict]  # [{metric, expected, actual, variance, pass/fail}]

    # Approvals (Human-in-Loop)
    approval_gates: List[dict]  # [{gate_name, status, approver, timestamp, decision, notes}]
    pending_approvals: List[str]

    # Outputs
    artifacts: List[dict]  # [{artifact_id, type, path, created_at, checksum}]
    expected_outputs: List[str]

    # Execution Metadata
    execution_log: List[dict]  # Immutable audit trail
    errors: List[dict]
    retry_count: int
    max_retries: int
```

#### Graph Node Implementations

**1. DQ Validation Node**
```python
async def data_quality_node(state: WorkOrderState) -> WorkOrderState:
    """
    Run DQ checks on all input datasets.
    Blocks if critical failures detected.
    """
    dq_service = DataQualityService()

    results = []
    for dataset_ref in state["input_datasets"]:
        dataset = await load_dataset(dataset_ref["dataset_id"])

        checks = await dq_service.run_checks(
            dataset=dataset,
            template_type=dataset_ref["template_type"],
            critical_threshold=0.95  # 95% pass rate required
        )

        results.append(checks)

    # Check for critical failures
    critical_failures = [
        r for r in results
        if r["critical_checks_failed"] > 0
    ]

    if critical_failures:
        state["errors"].append({
            "type": "dq_critical_failure",
            "details": critical_failures
        })
        state["current_stage"] = "failed"
        return state

    state["dq_results"] = results
    state["current_stage"] = "dq_completed"
    state["execution_log"].append({
        "timestamp": datetime.utcnow(),
        "node": "data_quality",
        "status": "completed",
        "checks_run": len(results)
    })

    # Notify via WebSocket
    await manager.send_work_order_update(
        tenant_id=state["tenant_id"],
        work_order_id=state["work_order_id"],
        update_type="stage_change",
        data={"new_stage": "dq_completed", "dq_summary": results}
    )

    return state
```

**2. Routing Logic Node**
```python
async def routing_node(state: WorkOrderState) -> str:
    """
    Determine which agent(s) to invoke based on objective.
    Can route to multiple agents in parallel if needed.
    """
    objective = state["objective"].lower()

    # Simple keyword-based routing (can be LLM-powered for complex cases)
    routing_map = {
        "cash": "cash_commander",
        "13-week": "cash_commander",
        "liquidity": "cash_commander",
        "close": "close_copilot",
        "reconciliation": "close_copilot",
        "margin": "margin_mechanic",
        "bridge": "margin_mechanic",
        "forecast": "forecast_factory",
        "scenario": "forecast_factory",
        "portfolio": "portfolio_allocator",
        "capital": "portfolio_allocator",
        "capex": "portfolio_allocator",
        "m&a": "deal_diligence",
        "deal": "deal_diligence"
    }

    for keyword, agent in routing_map.items():
        if keyword in objective:
            return agent

    # Default to general analysis
    return "general_analyst"
```

**3. Agent Executor Node**
```python
async def agent_executor_node(
    state: WorkOrderState,
    agent_name: str
) -> WorkOrderState:
    """
    Execute a specific finance agent with progress tracking.
    """
    agent = get_agent(agent_name)

    # Notify agent start
    await manager.send_agent_progress(
        tenant_id=state["tenant_id"],
        work_order_id=state["work_order_id"],
        agent_name=agent_name,
        progress_pct=0.0,
        current_step="Initializing..."
    )

    # Prepare agent inputs
    inputs = prepare_agent_inputs(
        datasets=state["input_datasets"],
        policy_refs=state["policy_refs"]
    )

    # Execute agent (async) with progress callbacks
    result = await agent.execute(
        inputs=inputs,
        progress_callback=lambda pct, step: manager.send_agent_progress(
            tenant_id=state["tenant_id"],
            work_order_id=state["work_order_id"],
            agent_name=agent_name,
            progress_pct=pct,
            current_step=step
        )
    )

    # Update state with agent output
    state["agent_outputs"][agent_name] = {
        "output": result.output,
        "confidence": result.confidence_score,
        "artifacts": result.artifacts,
        "execution_time_ms": result.execution_time,
        "llm_call_count": result.llm_call_count,
        "estimated_cost_usd": result.estimated_cost,
        "reasoning_trace": result.reasoning_trace
    }

    state["execution_log"].append({
        "timestamp": datetime.utcnow(),
        "node": f"agent_{agent_name}",
        "status": "completed",
        "confidence": result.confidence_score,
        "cost_usd": result.estimated_cost
    })

    # Notify agent completion
    await manager.send_work_order_update(
        tenant_id=state["tenant_id"],
        work_order_id=state["work_order_id"],
        update_type="agent_completed",
        data={
            "agent_name": agent_name,
            "confidence": result.confidence_score,
            "artifacts": result.artifacts
        }
    )

    return state
```

**4. Guardrail Enforcement Node**
```python
async def guardrail_node(state: WorkOrderState) -> WorkOrderState:
    """
    Enforce policy checks on agent outputs.
    Blocks execution if critical violations detected.
    """
    guardrail_agent = GuardrailAgent()
    policy_pack = await load_policy_pack(state["policy_refs"])

    checks = []
    for agent_name, output in state["agent_outputs"].items():
        check_results = await guardrail_agent.enforce_policies(
            agent_name=agent_name,
            agent_output=output,
            policies=policy_pack,
            context=state
        )
        checks.extend(check_results)

    state["guardrail_checks"] = checks

    # Check for critical violations
    critical_violations = [
        c for c in checks
        if c["severity"] == "critical" and c["status"] == "failed"
    ]

    if critical_violations:
        state["current_stage"] = "guardrail_blocked"
        state["pending_approvals"].append("override_guardrail")
        state["errors"].append({
            "type": "policy_violation",
            "critical_violations": critical_violations
        })
    else:
        state["current_stage"] = "guardrail_passed"

    return state
```

**5. Critic Validation Node**
```python
async def critic_node(state: WorkOrderState) -> WorkOrderState:
    """
    Statistical validation of agent outputs.
    Flags low-confidence outputs for supervisor review.
    """
    critic_agent = CriticAgent()

    validations = []
    for agent_name, output in state["agent_outputs"].items():
        validation = await critic_agent.validate(
            agent_name=agent_name,
            agent_output=output,
            historical_data=await load_historical_context(
                tenant_id=state["tenant_id"],
                agent_name=agent_name
            ),
            statistical_tests=[
                "outlier_detection",
                "variance_check",
                "reconciliation_check",
                "trend_consistency"
            ]
        )
        validations.append(validation)

    state["critic_validations"] = validations

    # Flag low-confidence outputs for review
    low_confidence = [
        v for v in validations
        if v["confidence"] < 0.7
    ]

    if low_confidence:
        state["pending_approvals"].append("supervisor_review_low_confidence")

    # Flag high variance vs. historical
    high_variance = [
        v for v in validations
        if abs(v.get("variance_pct", 0)) > 20
    ]

    if high_variance:
        state["pending_approvals"].append("explain_high_variance")

    return state
```

**6. Approval Gate Node**
```python
async def approval_gate_node(state: WorkOrderState) -> WorkOrderState:
    """
    Pause execution for human approval.
    Uses LangGraph's interrupt mechanism.
    """
    if state["pending_approvals"]:
        # Send notification to supervisors
        await send_approval_notification(
            work_order_id=state["work_order_id"],
            approvers=get_approvers_for_gates(state["pending_approvals"]),
            context={
                "objective": state["objective"],
                "agent_outputs": state["agent_outputs"],
                "guardrail_checks": state["guardrail_checks"],
                "critic_validations": state["critic_validations"]
            }
        )

        # LangGraph will pause here and resume when approved
        state["current_stage"] = "awaiting_approval"

        # Log approval request
        state["execution_log"].append({
            "timestamp": datetime.utcnow(),
            "node": "approval_gate",
            "status": "waiting",
            "gates": state["pending_approvals"]
        })
    else:
        state["current_stage"] = "approved"

    return state
```

**7. Artifact Generation Node**
```python
async def artifact_generation_node(state: WorkOrderState) -> WorkOrderState:
    """
    Generate final output artifacts (Excel, PDF, etc.)
    """
    artifact_gen = ArtifactGenerator()

    artifacts = []
    for expected_output in state["expected_outputs"]:
        artifact = await artifact_gen.generate(
            output_type=expected_output,
            agent_outputs=state["agent_outputs"],
            template_path=get_output_template(expected_output),
            tenant_id=state["tenant_id"]
        )

        # Save to filesystem (with tenant isolation)
        artifact_path = await save_artifact(
            artifact=artifact,
            work_order_id=state["work_order_id"],
            tenant_id=state["tenant_id"]
        )

        # Calculate checksum for integrity
        checksum = calculate_sha256(artifact_path)

        artifacts.append({
            "artifact_id": artifact.id,
            "type": expected_output,
            "path": artifact_path,
            "size_bytes": artifact.size,
            "checksum_sha256": checksum,
            "created_at": datetime.utcnow()
        })

    state["artifacts"] = artifacts
    state["current_stage"] = "completed"

    # Log completion
    state["execution_log"].append({
        "timestamp": datetime.utcnow(),
        "node": "artifact_generation",
        "status": "completed",
        "artifact_count": len(artifacts)
    })

    # Notify completion
    await manager.send_work_order_update(
        tenant_id=state["tenant_id"],
        work_order_id=state["work_order_id"],
        update_type="completed",
        data={
            "artifacts": artifacts,
            "execution_summary": {
                "total_time_ms": sum(
                    a["execution_time_ms"]
                    for a in state["agent_outputs"].values()
                ),
                "total_cost_usd": sum(
                    a["estimated_cost_usd"]
                    for a in state["agent_outputs"].values()
                ),
                "agents_executed": list(state["agent_outputs"].keys())
            }
        }
    )

    return state
```

#### Building the Graph

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

def build_work_order_graph() -> StateGraph:
    """Construct the LangGraph workflow"""

    # Initialize graph with PostgreSQL checkpointing
    checkpointer = PostgresSaver.from_conn_string(settings.database_url)
    graph = StateGraph(WorkOrderState, checkpointer=checkpointer)

    # Add nodes
    graph.add_node("dq_validation", data_quality_node)
    graph.add_node("routing", routing_node)
    graph.add_node("cash_commander", lambda s: agent_executor_node(s, "cash_commander"))
    graph.add_node("close_copilot", lambda s: agent_executor_node(s, "close_copilot"))
    graph.add_node("margin_mechanic", lambda s: agent_executor_node(s, "margin_mechanic"))
    graph.add_node("forecast_factory", lambda s: agent_executor_node(s, "forecast_factory"))
    graph.add_node("portfolio_allocator", lambda s: agent_executor_node(s, "portfolio_allocator"))
    graph.add_node("guardrail", guardrail_node)
    graph.add_node("critic", critic_node)
    graph.add_node("approval_gate", approval_gate_node)
    graph.add_node("artifact_generation", artifact_generation_node)

    # Add edges (workflow paths)
    graph.set_entry_point("dq_validation")
    graph.add_edge("dq_validation", "routing")

    # Conditional routing to agents
    graph.add_conditional_edges(
        "routing",
        lambda s: routing_node(s),  # Returns agent name
        {
            "cash_commander": "cash_commander",
            "close_copilot": "close_copilot",
            "margin_mechanic": "margin_mechanic",
            "forecast_factory": "forecast_factory",
            "portfolio_allocator": "portfolio_allocator",
            "general_analyst": "general_analyst"
        }
    )

    # All agents flow to guardrail
    for agent in ["cash_commander", "close_copilot", "margin_mechanic",
                  "forecast_factory", "portfolio_allocator", "general_analyst"]:
        graph.add_edge(agent, "guardrail")

    graph.add_edge("guardrail", "critic")
    graph.add_edge("critic", "approval_gate")

    # Conditional approval gate
    graph.add_conditional_edges(
        "approval_gate",
        lambda s: "approved" if s["current_stage"] == "approved" else "await",
        {
            "approved": "artifact_generation",
            "await": END  # Pause and wait for approval
        }
    )

    graph.add_edge("artifact_generation", END)

    return graph.compile()
```

---

## Layer 3: Agent Network

### Base Agent Architecture

All finance agents inherit from `BaseFinanceAgent`:

```python
from abc import ABC, abstractmethod
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Callable

class AgentOutput(BaseModel):
    """Standardized agent output format"""
    agent_name: str
    output: Dict[str, Any]
    confidence_score: float = Field(ge=0.0, le=1.0)
    artifacts: List[Dict[str, str]]  # [{artifact_id, path, type}]
    execution_time: float  # milliseconds
    llm_call_count: int
    estimated_cost: float  # USD
    reasoning_trace: List[str]  # For explainability

class BaseFinanceAgent(ABC):
    """Base class for all finance agents"""

    def __init__(
        self,
        agent_name: str,
        model_name: str = "openai/gpt-4-turbo",  # OpenRouter model ID
        temperature: float = 0.1,
        tools: List[Tool] = None
    ):
        self.agent_name = agent_name
        self.model_name = model_name
        self.temperature = temperature

        # Initialize LLM via OpenRouter
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
            model=model_name,
            temperature=temperature,
            model_kwargs={
                "headers": {
                    "HTTP-Referer": "https://agenticcfo.com",
                    "X-Title": "AgenticCFO Platform"
                }
            }
        )

        # Initialize tools
        self.tools = tools or self.get_default_tools()

        # Create agent
        self.agent = self._create_agent()

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass

    @abstractmethod
    def get_default_tools(self) -> List[Tool]:
        """Return the default tools for this agent"""
        pass

    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent executor"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            max_iterations=10,
            handle_parsing_errors=True
        )

    async def execute(
        self,
        inputs: Dict[str, Any],
        policy_constraints: Dict[str, Any] = None,
        progress_callback: Callable[[float, str], None] = None
    ) -> AgentOutput:
        """Execute the agent with given inputs"""
        import time
        start_time = time.time()

        # Prepare input with policy constraints
        agent_input = self._prepare_input(inputs, policy_constraints)

        # Execute agent
        if progress_callback:
            progress_callback(10.0, "Starting analysis...")

        result = await self.agent.ainvoke(agent_input)

        if progress_callback:
            progress_callback(90.0, "Generating outputs...")

        # Extract reasoning trace
        reasoning_trace = [
            step[0].log for step in result.get("intermediate_steps", [])
        ]

        # Calculate execution metrics
        execution_time = (time.time() - start_time) * 1000
        llm_call_count = len(result.get("intermediate_steps", []))

        # Parse output and generate artifacts
        parsed_output = self._parse_output(result["output"])
        artifacts = await self._generate_artifacts(parsed_output)

        if progress_callback:
            progress_callback(100.0, "Completed")

        return AgentOutput(
            agent_name=self.agent_name,
            output=parsed_output,
            confidence_score=self._calculate_confidence(parsed_output, reasoning_trace),
            artifacts=artifacts,
            execution_time=execution_time,
            llm_call_count=llm_call_count,
            estimated_cost=self._estimate_cost(self.model_name, llm_call_count),
            reasoning_trace=reasoning_trace
        )

    @abstractmethod
    def _prepare_input(self, inputs: Dict, policy_constraints: Dict) -> Dict:
        """Prepare inputs for agent execution"""
        pass

    @abstractmethod
    def _parse_output(self, raw_output: str) -> Dict:
        """Parse agent output into structured format"""
        pass

    @abstractmethod
    async def _generate_artifacts(self, parsed_output: Dict) -> List[Dict]:
        """Generate output artifacts (Excel files, PDFs, etc.)"""
        pass

    def _calculate_confidence(self, output: Dict, reasoning: List[str]) -> float:
        """Calculate confidence score (0-1) based on output and reasoning quality"""
        base_confidence = 0.8

        # Penalize if few reasoning steps
        if len(reasoning) < 3:
            base_confidence -= 0.2

        # Check for uncertainty keywords
        uncertainty_keywords = ["unsure", "unclear", "might", "possibly", "perhaps", "estimate", "approximately"]
        uncertainty_count = sum(
            1 for step in reasoning
            for keyword in uncertainty_keywords
            if keyword in step.lower()
        )
        base_confidence -= (uncertainty_count * 0.05)

        # Check for missing expected fields in output
        expected_fields = ["summary", "recommendations", "data"]
        missing_fields = [f for f in expected_fields if f not in output]
        base_confidence -= (len(missing_fields) * 0.1)

        return max(0.0, min(1.0, base_confidence))

    def _estimate_cost(self, model_name: str, llm_calls: int) -> float:
        """Estimate execution cost in USD based on model and calls"""
        # OpenRouter pricing (approximate)
        pricing = {
            "openai/gpt-4-turbo": 0.02,  # per call
            "openai/gpt-3.5-turbo": 0.002,
            "anthropic/claude-3.5-sonnet": 0.015,
            "meta-llama/llama-3.1-70b-instruct": 0.005
        }
        return pricing.get(model_name, 0.01) * llm_calls
```

### Example Agent: Cash Commander

```python
from langchain.tools import Tool
import pandas as pd
from typing import Dict, Any, List

class CashCommanderAgent(BaseFinanceAgent):
    """
    Agent for cash forecasting and liquidity management.

    Responsibilities:
    - Analyze bank statements to determine cash position
    - Review AP/AR to forecast inflows/outflows
    - Generate 13-week rolling cash forecast
    - Identify liquidity early warnings (covenant breaches, min cash violations)
    - Recommend cash optimization actions
    """

    def __init__(self):
        super().__init__(
            agent_name="cash_commander",
            model_name="openai/gpt-4-turbo",  # Use GPT-4 for complex financial reasoning
            temperature=0.1  # Low temperature for consistency
        )

    def get_system_prompt(self) -> str:
        return """You are Cash Commander, an expert treasury agent specializing in
        cash forecasting and liquidity management.

        Your responsibilities:
        1. Analyze bank statements to determine current cash position
        2. Review AP/AR open items to forecast cash inflows and outflows
        3. Generate a 13-week rolling cash forecast with confidence intervals
        4. Identify liquidity early warnings (covenant breaches, minimum cash violations)
        5. Recommend cash optimization actions (accelerate collections, optimize DPO)

        You MUST:
        - Reconcile bank balances to GL cash accounts within 1% tolerance
        - Flag any discrepancies or unusual patterns (large withdrawals, unexpected fees)
        - Calculate daily cash positions with 80% and 95% confidence intervals
        - Check against minimum cash policies and debt covenants
        - Provide variance explanations vs. prior forecast

        Output Format (JSON):
        {
            "cash_position": {
                "opening_balance": float,
                "closing_balance": float,
                "currency": "USD",
                "as_of_date": "YYYY-MM-DD"
            },
            "13_week_forecast": [
                {
                    "week": int,
                    "week_start": "YYYY-MM-DD",
                    "inflows": float,
                    "outflows": float,
                    "net": float,
                    "ending_balance": float,
                    "confidence_80": {"low": float, "high": float},
                    "confidence_95": {"low": float, "high": float}
                },
                ...
            ],
            "liquidity_warnings": [
                {
                    "type": "min_cash_breach" | "covenant_breach" | "high_burn",
                    "date": "YYYY-MM-DD",
                    "severity": "high" | "medium" | "low",
                    "description": str,
                    "amount": float
                }
            ],
            "reconciliation": {
                "bank_balance": float,
                "gl_balance": float,
                "variance": float,
                "variance_pct": float,
                "reconciled": bool
            },
            "recommendations": [
                {
                    "action": str,
                    "impact_usd": float,
                    "timeframe": str,
                    "priority": "high" | "medium" | "low"
                }
            ],
            "variance_vs_prior": {
                "prior_forecast_date": "YYYY-MM-DD",
                "week_2_variance_pct": float,
                "explanation": str
            }
        }

        Use the provided tools to analyze data. Be precise and conservative in forecasts.
        Always explain your reasoning and flag uncertainties."""

    def get_default_tools(self) -> List[Tool]:
        """Tools for cash analysis"""
        return [
            Tool(
                name="analyze_bank_statement",
                func=self._analyze_bank_statement,
                description="Analyze a bank statement file to extract cash positions, transactions, and trends. Input: dataset_id (UUID)"
            ),
            Tool(
                name="analyze_ap_open_items",
                func=self._analyze_ap_open_items,
                description="Analyze AP open items to forecast cash outflows by week. Input: dataset_id (UUID)"
            ),
            Tool(
                name="analyze_ar_open_items",
                func=self._analyze_ar_open_items,
                description="Analyze AR open items to forecast cash inflows by week with collection probability. Input: dataset_id (UUID)"
            ),
            Tool(
                name="get_gl_cash_balance",
                func=self._get_gl_cash_balance,
                description="Get GL cash account balance from trial balance. Input: dataset_id (UUID), account_number (str)"
            ),
            Tool(
                name="calculate_cash_forecast",
                func=self._calculate_cash_forecast,
                description="Calculate 13-week cash forecast using inflows/outflows data with Monte Carlo simulation. Input: JSON with opening_balance, weekly_inflows[], weekly_outflows[]"
            ),
            Tool(
                name="check_covenant_compliance",
                func=self._check_covenant_compliance,
                description="Check cash balance against covenant requirements and minimum cash policies. Input: cash_balance (float), policy_id (str)"
            ),
            Tool(
                name="get_historical_forecast_accuracy",
                func=self._get_historical_forecast_accuracy,
                description="Get historical forecast accuracy metrics for variance analysis. Input: tenant_id (str), weeks_back (int)"
            )
        ]

    def _analyze_bank_statement(self, dataset_id: str) -> str:
        """Analyze bank statement data"""
        dataset = load_dataset_from_db(dataset_id)
        df = pd.DataFrame(dataset["data"])

        # Extract key metrics
        opening_balance = df.iloc[0]["opening_balance"] if "opening_balance" in df.columns else df.iloc[0]["balance"]
        closing_balance = df.iloc[-1]["closing_balance"] if "closing_balance" in df.columns else df.iloc[-1]["balance"]

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        total_inflows = df[df["amount"] > 0]["amount"].sum()
        total_outflows = abs(df[df["amount"] < 0]["amount"].sum())

        # Detect patterns
        avg_daily_burn = total_outflows / len(df) if len(df) > 0 else 0
        large_transactions = df[abs(df["amount"]) > (df["amount"].std() * 2)]

        return json.dumps({
            "opening_balance": float(opening_balance),
            "closing_balance": float(closing_balance),
            "total_inflows": float(total_inflows),
            "total_outflows": float(total_outflows),
            "net_change": float(closing_balance - opening_balance),
            "avg_daily_burn": float(avg_daily_burn),
            "transaction_count": len(df),
            "large_transactions": large_transactions.to_dict("records"),
            "currency": dataset.get("currency", "USD"),
            "period_days": len(df)
        })

    def _analyze_ap_open_items(self, dataset_id: str) -> str:
        """Analyze AP to forecast outflows"""
        dataset = load_dataset_from_db(dataset_id)
        df = pd.DataFrame(dataset["data"])

        df["due_date"] = pd.to_datetime(df["due_date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        today = pd.Timestamp.now()

        # Forecast by week
        weekly_outflows = []
        for week in range(13):
            week_start = today + pd.Timedelta(weeks=week)
            week_end = week_start + pd.Timedelta(days=7)

            week_amount = df[
                (df["due_date"] >= week_start) & (df["due_date"] < week_end)
            ]["amount"].sum()

            # Apply payment probability (e.g., early-pay discounts, typical payment patterns)
            payment_probability = 0.95  # 95% of invoices paid on time

            weekly_outflows.append({
                "week": week + 1,
                "week_start": week_start.strftime("%Y-%m-%d"),
                "amount": float(week_amount),
                "expected_amount": float(week_amount * payment_probability),
                "invoice_count": len(df[(df["due_date"] >= week_start) & (df["due_date"] < week_end)])
            })

        return json.dumps({
            "total_ap": float(df["amount"].sum()),
            "weekly_forecast": weekly_outflows,
            "past_due_amount": float(df[df["due_date"] < today]["amount"].sum()),
            "vendor_count": df["vendor_id"].nunique() if "vendor_id" in df.columns else 0
        })

    def _analyze_ar_open_items(self, dataset_id: str) -> str:
        """Analyze AR to forecast inflows"""
        dataset = load_dataset_from_db(dataset_id)
        df = pd.DataFrame(dataset["data"])

        df["due_date"] = pd.to_datetime(df["due_date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        today = pd.Timestamp.now()

        # Calculate aging for collection probability
        df["days_outstanding"] = (today - df["invoice_date"]).dt.days if "invoice_date" in df.columns else 0

        # Collection probability curve (based on aging)
        def collection_probability(days_outstanding):
            if days_outstanding <= 30:
                return 0.95
            elif days_outstanding <= 60:
                return 0.80
            elif days_outstanding <= 90:
                return 0.60
            else:
                return 0.30

        df["collection_prob"] = df["days_outstanding"].apply(collection_probability)

        # Forecast by week
        weekly_inflows = []
        for week in range(13):
            week_start = today + pd.Timedelta(weeks=week)
            week_end = week_start + pd.Timedelta(days=7)

            week_invoices = df[
                (df["due_date"] >= week_start) & (df["due_date"] < week_end)
            ]

            week_amount = week_invoices["amount"].sum()
            expected_amount = (week_invoices["amount"] * week_invoices["collection_prob"]).sum()

            weekly_inflows.append({
                "week": week + 1,
                "week_start": week_start.strftime("%Y-%m-%d"),
                "amount": float(week_amount),
                "expected_amount": float(expected_amount),
                "invoice_count": len(week_invoices),
                "avg_collection_prob": float(week_invoices["collection_prob"].mean()) if len(week_invoices) > 0 else 0
            })

        return json.dumps({
            "total_ar": float(df["amount"].sum()),
            "weekly_forecast": weekly_inflows,
            "past_due_amount": float(df[df["due_date"] < today]["amount"].sum()),
            "customer_count": df["customer_id"].nunique() if "customer_id" in df.columns else 0,
            "weighted_dso": float((df["amount"] * df["days_outstanding"]).sum() / df["amount"].sum()) if df["amount"].sum() > 0 else 0
        })

    def _get_gl_cash_balance(self, dataset_id: str, account_number: str = "1010") -> str:
        """Get GL cash balance from trial balance"""
        dataset = load_dataset_from_db(dataset_id)
        df = pd.DataFrame(dataset["data"])

        # Normalize column names
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Find cash account
        cash_account = df[df["account_number"].astype(str) == str(account_number)]

        if cash_account.empty:
            # Try searching by account name
            cash_account = df[df["account_name"].str.contains("cash", case=False, na=False)]

        if cash_account.empty:
            return json.dumps({"error": f"Cash account {account_number} not found in trial balance"})

        balance = cash_account.iloc[0]["balance"] if "balance" in cash_account.columns else cash_account.iloc[0]["balance_funccurr"]

        return json.dumps({
            "account_number": str(cash_account.iloc[0]["account_number"]),
            "account_name": cash_account.iloc[0]["account_name"],
            "balance": float(balance),
            "currency": cash_account.iloc[0].get("currency", "USD"),
            "period": cash_account.iloc[0].get("period", "Unknown")
        })

    def _calculate_cash_forecast(self, forecast_input: str) -> str:
        """Calculate 13-week cash forecast with Monte Carlo simulation"""
        import json
        import numpy as np

        data = json.loads(forecast_input)

        opening_balance = data["opening_balance"]
        weekly_inflows = data["weekly_inflows"]  # [{week, amount}]
        weekly_outflows = data["weekly_outflows"]  # [{week, amount}]

        # Monte Carlo parameters
        n_simulations = 1000
        inflow_volatility = 0.15  # 15% standard deviation
        outflow_volatility = 0.10  # 10% standard deviation

        forecast = []
        running_balance = opening_balance

        for week in range(13):
            week_inflow_base = weekly_inflows[week]["expected_amount"] if week < len(weekly_inflows) else 0
            week_outflow_base = weekly_outflows[week]["expected_amount"] if week < len(weekly_outflows) else 0

            # Run Monte Carlo simulations
            simulated_balances = []
            for _ in range(n_simulations):
                sim_inflow = np.random.normal(week_inflow_base, week_inflow_base * inflow_volatility)
                sim_outflow = np.random.normal(week_outflow_base, week_outflow_base * outflow_volatility)
                sim_balance = running_balance + sim_inflow - sim_outflow
                simulated_balances.append(sim_balance)

            # Calculate confidence intervals
            percentile_80_low = np.percentile(simulated_balances, 10)
            percentile_80_high = np.percentile(simulated_balances, 90)
            percentile_95_low = np.percentile(simulated_balances, 2.5)
            percentile_95_high = np.percentile(simulated_balances, 97.5)

            week_net = week_inflow_base - week_outflow_base
            running_balance += week_net

            forecast.append({
                "week": week + 1,
                "inflows": week_inflow_base,
                "outflows": week_outflow_base,
                "net": week_net,
                "ending_balance": running_balance,
                "confidence_80": {"low": percentile_80_low, "high": percentile_80_high},
                "confidence_95": {"low": percentile_95_low, "high": percentile_95_high}
            })

        return json.dumps({"forecast": forecast})

    def _check_covenant_compliance(self, cash_balance: str, policy_id: str) -> str:
        """Check covenant compliance"""
        balance = float(cash_balance)

        # Load policy from database
        policy = load_policy_from_db(policy_id)
        min_cash = policy.get("minimum_cash_balance", 0)
        min_liquidity_ratio = policy.get("minimum_liquidity_ratio", 1.0)
        debt_covenants = policy.get("debt_covenants", [])

        compliance_checks = []

        # Check minimum cash
        min_cash_compliant = balance >= min_cash
        compliance_checks.append({
            "check": "minimum_cash",
            "compliant": min_cash_compliant,
            "current": balance,
            "required": min_cash,
            "headroom": balance - min_cash,
            "headroom_pct": ((balance - min_cash) / min_cash * 100) if min_cash > 0 else 100
        })

        # Check debt covenants (if applicable)
        for covenant in debt_covenants:
            if covenant["type"] == "min_cash":
                covenant_compliant = balance >= covenant["threshold"]
                compliance_checks.append({
                    "check": f"covenant_{covenant['name']}",
                    "compliant": covenant_compliant,
                    "current": balance,
                    "required": covenant["threshold"],
                    "headroom": balance - covenant["threshold"]
                })

        overall_compliant = all(c["compliant"] for c in compliance_checks)

        return json.dumps({
            "overall_compliant": overall_compliant,
            "checks": compliance_checks,
            "warnings": [c for c in compliance_checks if not c["compliant"]]
        })

    def _get_historical_forecast_accuracy(self, tenant_id: str, weeks_back: int = 4) -> str:
        """Get historical forecast accuracy"""
        # Query historical forecasts and actuals
        historical_data = query_historical_forecasts(tenant_id, weeks_back)

        if not historical_data:
            return json.dumps({"error": "No historical data available"})

        # Calculate MAPE (Mean Absolute Percentage Error)
        errors = []
        for record in historical_data:
            actual = record["actual_cash"]
            forecast = record["forecast_cash"]
            if actual != 0:
                ape = abs((actual - forecast) / actual) * 100
                errors.append(ape)

        mape = np.mean(errors) if errors else 0

        return json.dumps({
            "mape_pct": mape,
            "forecast_count": len(historical_data),
            "weeks_analyzed": weeks_back,
            "latest_forecast_date": historical_data[-1]["forecast_date"] if historical_data else None,
            "accuracy_rating": "Excellent" if mape < 5 else "Good" if mape < 10 else "Fair" if mape < 20 else "Needs Improvement"
        })

    def _prepare_input(self, inputs: Dict, policy_constraints: Dict) -> Dict:
        """Prepare agent input"""
        # Format datasets
        datasets_info = "\n".join([
            f"- {ds['template_type']} (ID: {ds['dataset_id']}, Period: {ds.get('period', 'N/A')})"
            for ds in inputs.get("datasets", [])
        ])

        # Format policies
        policies_info = "\n".join([
            f"- {policy}" for policy in policy_constraints.get("policies", [])
        ]) if policy_constraints else "No specific policies"

        return {
            "input": f"""Analyze the following datasets and generate a comprehensive 13-week cash forecast with liquidity warnings.

**Available Datasets:**
{datasets_info}

**Policy Constraints:**
{policies_info}

**Instructions:**
1. Analyze the bank statement to get the current cash position
2. Review AP open items to forecast cash outflows (apply payment probability)
3. Review AR open items to forecast cash inflows (apply collection probability based on aging)
4. Calculate the 13-week rolling forecast using Monte Carlo simulation for confidence intervals
5. Reconcile bank balance to GL cash account (within 1% tolerance)
6. Check covenant compliance and minimum cash requirements
7. Identify any liquidity warnings (min cash breach, covenant breach, high burn rate)
8. Compare forecast to prior period and explain significant variances
9. Provide actionable recommendations for cash optimization

**Be thorough and explain your reasoning at each step. Flag any uncertainties or data quality issues.**"""
        }

    def _parse_output(self, raw_output: str) -> Dict:
        """Parse agent output"""
        import json
        import re

        # Try to extract JSON from output
        json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Fallback: return raw output with error flag
        return {
            "error": "Failed to parse structured output",
            "raw_output": raw_output
        }

    async def _generate_artifacts(self, parsed_output: Dict) -> List[Dict]:
        """Generate Excel artifacts"""
        import uuid
        from openpyxl import Workbook
        import os

        artifacts = []

        # Generate Cash_Ladder.xlsx
        if "13_week_forecast" in parsed_output:
            wb = Workbook()
            ws = wb.active
            ws.title = "13-Week Forecast"

            # Headers
            ws.append([
                "Week", "Week Start", "Inflows", "Outflows", "Net",
                "Ending Balance", "80% CI Low", "80% CI High",
                "95% CI Low", "95% CI High"
            ])

            # Data
            for week_data in parsed_output["13_week_forecast"]:
                ws.append([
                    week_data.get("week"),
                    week_data.get("week_start"),
                    week_data.get("inflows", 0),
                    week_data.get("outflows", 0),
                    week_data.get("net", 0),
                    week_data.get("ending_balance", 0),
                    week_data.get("confidence_80", {}).get("low", 0),
                    week_data.get("confidence_80", {}).get("high", 0),
                    week_data.get("confidence_95", {}).get("low", 0),
                    week_data.get("confidence_95", {}).get("high", 0)
                ])

            # Save to filesystem
            file_path = f"/tmp/artifacts/Cash_Ladder_{uuid.uuid4()}.xlsx"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            wb.save(file_path)

            artifacts.append({
                "artifact_id": str(uuid.uuid4()),
                "type": "Cash_Ladder.xlsx",
                "path": file_path
            })

        # Generate Liquidity_Warnings.pdf (stub)
        if "liquidity_warnings" in parsed_output and parsed_output["liquidity_warnings"]:
            # Would use reportlab or similar for PDF generation
            file_path = f"/tmp/artifacts/Liquidity_Warnings_{uuid.uuid4()}.pdf"
            artifacts.append({
                "artifact_id": str(uuid.uuid4()),
                "type": "Liquidity_Warnings.pdf",
                "path": file_path
            })

        return artifacts
```

### Other Key Agents (Summaries)

**Close Copilot:**
- Auto-reconciles bank-to-GL, AR/AP subledger-to-control
- Proposes accruals based on historical patterns
- Generates close checklist with Day-N status
- Tools: reconciliation_engine, accrual_recommender, variance_analyzer

**Margin Mechanic:**
- Builds Price/Volume/Mix bridges
- Decomposes inflation vs. productivity
- Analyzes gross margin by BU/SKU/channel
- Tools: pvm_decomposer, inflation_indexer, margin_waterfall_builder

**Forecast Factory:**
- Rolling forecast using driver-based models
- Scenario trees (base/upside/downside)
- Variance explanations vs. prior forecast
- Tools: time_series_forecaster, scenario_simulator, variance_explainer

**Portfolio Allocator:**
- Ranks projects by EVA/NPV/IRR
- Applies risk-adjusted screens
- Solves capital envelope optimization
- Tools: dcf_calculator, wacc_calculator, capital_optimizer

**Guardrail Agent:**
- Enforces materiality thresholds
- Checks SoD violations
- Validates treasury limits (min cash, max exposure)
- Applies disclosure gates
- Tools: policy_parser, sod_checker, limit_validator

**Critic Agent:**
- Statistical validation (outlier detection, variance checks)
- Reconciliation verification
- Trend consistency checks
- Confidence scoring
- Tools: outlier_detector, reconciliation_verifier, trend_analyzer

**Compliance Scribe:**
- Compiles audit logs
- Generates evidence bundles (ZIP with artifacts + logs + policies)
- Exports disclosure checklists
- Tools: log_compiler, evidence_bundler, disclosure_generator

---

## Layer 4: LLM & Tool Layer

### OpenRouter Multi-Model Strategy

```python
# Model selection matrix
MODEL_MATRIX = {
    # Complex reasoning, capital allocation, M&A valuation
    "complex_reasoning": "openai/gpt-4-turbo",

    # Data analysis, margin mechanics, cost decomposition
    "data_analysis": "anthropic/claude-3.5-sonnet",

    # Routine tasks, DQ checks, workbook auditing
    "routine": "openai/gpt-3.5-turbo",

    # Bulk processing, cost optimization
    "bulk": "meta-llama/llama-3.1-70b-instruct"
}

# Agent-to-model mapping
AGENT_MODEL_MAP = {
    "cash_commander": "openai/gpt-4-turbo",
    "close_copilot": "openai/gpt-3.5-turbo",
    "margin_mechanic": "anthropic/claude-3.5-sonnet",
    "forecast_factory": "openai/gpt-4-turbo",
    "portfolio_allocator": "openai/gpt-4-turbo",
    "deal_diligence": "openai/gpt-4-turbo",
    "guardrail": "openai/gpt-3.5-turbo",
    "critic": "anthropic/claude-3.5-sonnet",
    "workbook_auditor": "openai/gpt-3.5-turbo",
    "compliance_scribe": "openai/gpt-3.5-turbo"
}
```

### Custom Finance Tools

```python
from langchain.tools import Tool

def create_npv_calculator_tool() -> Tool:
    """NPV calculator for capital projects"""

    def calculate_npv(input_json: str) -> str:
        import json
        import numpy as np

        data = json.loads(input_json)
        cashflows = data["cashflows"]  # List of annual cashflows
        discount_rate = data["discount_rate"]  # WACC

        npv = sum(
            cf / ((1 + discount_rate) ** i)
            for i, cf in enumerate(cashflows)
        )

        # Calculate IRR
        try:
            irr = np.irr(cashflows)
        except:
            irr = None

        return json.dumps({
            "npv": npv,
            "irr": irr,
            "payback_period": calculate_payback(cashflows),
            "profitability_index": (npv + abs(cashflows[0])) / abs(cashflows[0])
        })

    return Tool(
        name="calculate_npv",
        func=calculate_npv,
        description="Calculate NPV, IRR, and payback period for a capital project. Input: JSON with cashflows[] and discount_rate"
    )

def create_wacc_calculator_tool() -> Tool:
    """WACC calculator"""

    def calculate_wacc(input_json: str) -> str:
        import json

        data = json.loads(input_json)
        equity_value = data["equity_value"]
        debt_value = data["debt_value"]
        cost_of_equity = data["cost_of_equity"]  # CAPM
        cost_of_debt = data["cost_of_debt"]
        tax_rate = data["tax_rate"]

        total_value = equity_value + debt_value
        equity_weight = equity_value / total_value
        debt_weight = debt_value / total_value

        wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))

        return json.dumps({
            "wacc": wacc,
            "equity_weight": equity_weight,
            "debt_weight": debt_weight,
            "after_tax_cost_of_debt": cost_of_debt * (1 - tax_rate)
        })

    return Tool(
        name="calculate_wacc",
        func=calculate_wacc,
        description="Calculate WACC for capital allocation decisions. Input: JSON with equity_value, debt_value, cost_of_equity, cost_of_debt, tax_rate"
    )
```

### ChromaDB Integration (Mapping Memory)

```python
import chromadb
from chromadb.config import Settings

class MappingMemoryService:
    """Service for semantic column matching using ChromaDB"""

    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory=settings.chroma_persist_directory,
            anonymized_telemetry=False
        ))

        self.collection = self.client.get_or_create_collection(
            name="column_mappings",
            metadata={"description": "Template column mappings with embeddings"}
        )

    async def find_similar_columns(
        self,
        source_column: str,
        template_type: str,
        top_k: int = 3
    ) -> List[Dict]:
        """Find similar template columns using semantic search"""

        results = self.collection.query(
            query_texts=[source_column],
            n_results=top_k,
            where={"template_type": template_type}
        )

        matches = []
        for i, doc_id in enumerate(results["ids"][0]):
            matches.append({
                "template_column": results["metadatas"][0][i]["template_column"],
                "similarity_score": 1 - results["distances"][0][i],  # Convert distance to similarity
                "example_values": results["metadatas"][0][i].get("example_values", [])
            })

        return matches

    async def store_mapping(
        self,
        tenant_id: str,
        template_type: str,
        source_column: str,
        template_column: str,
        example_values: List[str] = None
    ):
        """Store a confirmed mapping for future reuse"""

        doc_id = f"{tenant_id}_{template_type}_{source_column}"

        self.collection.add(
            ids=[doc_id],
            documents=[f"{source_column} maps to {template_column}"],
            metadatas=[{
                "tenant_id": tenant_id,
                "template_type": template_type,
                "source_column": source_column,
                "template_column": template_column,
                "example_values": example_values or []
            }]
        )
```

---

## Layer 5: Output & Audit Layer

### Artifact Generation

```python
class ArtifactGenerator:
    """Generate output artifacts (Excel, PDF, Word)"""

    async def generate(
        self,
        output_type: str,
        agent_outputs: Dict[str, Any],
        template_path: str,
        tenant_id: str
    ) -> Artifact:
        """
        Generate artifact based on type.

        Supported types:
        - Cash_Ladder.xlsx
        - 13W_Forecast.xlsx
        - GM_Bridge_BU_SKU.xlsx
        - Forecast_Rolling.xlsx
        - Portfolio_Ranked.xlsx
        - Liquidity_Warnings.pdf
        - Investment_Memo.docx
        """

        if output_type.endswith(".xlsx"):
            return await self._generate_excel(output_type, agent_outputs, template_path)
        elif output_type.endswith(".pdf"):
            return await self._generate_pdf(output_type, agent_outputs, template_path)
        elif output_type.endswith(".docx"):
            return await self._generate_word(output_type, agent_outputs, template_path)
        else:
            raise ValueError(f"Unsupported output type: {output_type}")

    async def _generate_excel(
        self,
        output_type: str,
        agent_outputs: Dict,
        template_path: str
    ) -> Artifact:
        """Generate Excel artifact using openpyxl"""
        from openpyxl import load_workbook

        # Load template (if exists)
        if os.path.exists(template_path):
            wb = load_workbook(template_path)
        else:
            wb = Workbook()

        # Populate based on output type
        if output_type == "Cash_Ladder.xlsx":
            ws = wb.active
            ws.title = "Cash Ladder"

            # Headers
            ws.append(["Week", "Inflows", "Outflows", "Net", "Ending Balance"])

            # Data from Cash Commander
            cash_output = agent_outputs.get("cash_commander", {}).get("output", {})
            for week_data in cash_output.get("13_week_forecast", []):
                ws.append([
                    week_data["week"],
                    week_data["inflows"],
                    week_data["outflows"],
                    week_data["net"],
                    week_data["ending_balance"]
                ])

        # Save to temp file
        temp_path = f"/tmp/{output_type}"
        wb.save(temp_path)

        return Artifact(
            id=str(uuid.uuid4()),
            type=output_type,
            path=temp_path,
            size=os.path.getsize(temp_path),
            created_at=datetime.utcnow()
        )
```

### Audit Logging

```python
class AuditLogService:
    """Immutable audit logging for compliance"""

    async def log_event(
        self,
        event_type: str,
        tenant_id: str,
        user_id: str,
        work_order_id: str,
        details: Dict[str, Any]
    ):
        """Log an immutable audit event"""

        event = AuditEvent(
            id=uuid.uuid4(),
            event_type=event_type,
            tenant_id=tenant_id,
            user_id=user_id,
            work_order_id=work_order_id,
            details=details,
            timestamp=datetime.utcnow()
        )

        # Insert into PostgreSQL (append-only, no updates/deletes)
        await db.execute(
            """
            INSERT INTO audit_events
            (id, event_type, tenant_id, user_id, work_order_id, details, timestamp)
            VALUES (:id, :event_type, :tenant_id, :user_id, :work_order_id, :details, :timestamp)
            """,
            {
                "id": event.id,
                "event_type": event.event_type,
                "tenant_id": event.tenant_id,
                "user_id": event.user_id,
                "work_order_id": event.work_order_id,
                "details": json.dumps(event.details),
                "timestamp": event.timestamp
            }
        )

        # Also write to append-only log file for disaster recovery
        with open(f"/var/log/agenticcfo/audit_{tenant_id}.jsonl", "a") as f:
            f.write(json.dumps(asdict(event)) + "\n")
```

---

## Database Architecture

### Core Tables

```sql
-- File uploads
CREATE TABLE file_uploads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    filename VARCHAR(500) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,  -- SHA-256
    file_size_bytes BIGINT NOT NULL,
    upload_channel VARCHAR(50),  -- 'web', 'sftp', 'email'
    uploaded_by UUID REFERENCES users(id),
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    virus_scan_status VARCHAR(20),  -- 'clean', 'infected', 'pending'
    workbook_risk_score DECIMAL(3,2),  -- 0.00 to 1.00
    status VARCHAR(50),  -- 'uploaded', 'processing', 'staged', 'failed'
    error_message TEXT,
    INDEX idx_tenant_uploaded (tenant_id, uploaded_at DESC)
);

-- Dataset versioning
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    file_upload_id UUID REFERENCES file_uploads(id),
    template_type VARCHAR(100),  -- 'TrialBalance', 'AP_OpenItems', etc.
    entity VARCHAR(100),
    period_start DATE,
    period_end DATE,
    version INTEGER NOT NULL,
    row_count BIGINT,
    data_hash VARCHAR(64),  -- Hash of actual data values
    mapping_config_id UUID REFERENCES mapping_configs(id),
    dq_status VARCHAR(50),  -- 'passed', 'failed', 'warnings'
    dq_results JSONB,
    staged_data JSONB,  -- Actual data (for smaller datasets, else S3)
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(tenant_id, template_type, entity, period_start, version),
    INDEX idx_tenant_template_period (tenant_id, template_type, period_end DESC)
);

-- Mapping configurations
CREATE TABLE mapping_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    template_type VARCHAR(100),
    source_file_pattern VARCHAR(500),
    column_mappings JSONB NOT NULL,  -- {source_col: template_col}
    date_formats JSONB,
    currency_rules JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMP,
    use_count INTEGER DEFAULT 1,
    INDEX idx_tenant_template (tenant_id, template_type)
);

-- Work orders
CREATE TABLE work_orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    objective VARCHAR(500) NOT NULL,
    priority VARCHAR(20),  -- 'high', 'medium', 'low'
    input_datasets JSONB NOT NULL,  -- [{dataset_id, template_type, version}]
    policy_refs JSONB,
    current_stage VARCHAR(50),
    agent_outputs JSONB,
    dq_results JSONB,
    guardrail_checks JSONB,
    critic_validations JSONB,
    approval_gates JSONB,
    pending_approvals JSONB,
    artifacts JSONB,
    expected_outputs JSONB,
    execution_log JSONB,  -- Immutable audit trail
    errors JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    sla_deadline TIMESTAMP,
    INDEX idx_tenant_created (tenant_id, created_at DESC),
    INDEX idx_tenant_stage (tenant_id, current_stage)
);

-- Audit events (append-only)
CREATE TABLE audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    user_id UUID REFERENCES users(id),
    work_order_id UUID REFERENCES work_orders(id),
    details JSONB NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    INDEX idx_tenant_timestamp (tenant_id, timestamp DESC),
    INDEX idx_work_order (work_order_id, timestamp DESC)
);

-- Policy packs
CREATE TABLE policy_packs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    version INTEGER NOT NULL,
    policy_data JSONB NOT NULL,  -- Parsed Policy_Pack.xlsx
    effective_from DATE NOT NULL,
    effective_to DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    UNIQUE(tenant_id, version),
    INDEX idx_tenant_effective (tenant_id, effective_from DESC)
);

-- Artifacts
CREATE TABLE artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    work_order_id UUID NOT NULL REFERENCES work_orders(id),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    artifact_type VARCHAR(100),  -- 'Cash_Ladder.xlsx', 'Liquidity_Warnings.pdf'
    file_path VARCHAR(1000),
    file_size_bytes BIGINT,
    checksum_sha256 VARCHAR(64),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    INDEX idx_work_order (work_order_id),
    INDEX idx_tenant_created (tenant_id, created_at DESC)
);

-- Tenants (multi-tenancy)
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    settings JSONB,  -- Tenant-specific settings
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Users (existing, enhanced)
ALTER TABLE users ADD COLUMN tenant_id UUID REFERENCES tenants(id);
ALTER TABLE users ADD COLUMN role VARCHAR(50);  -- 'admin', 'cfo', 'controller', 'treasurer', 'analyst'
ALTER TABLE users ADD COLUMN approval_authority JSONB;  -- {gates: ['covenant_review', 'high_variance']}
```

---

## Real-Time WebSocket Updates

### WebSocket Manager

```python
from fastapi import WebSocket
from typing import Dict
import json

class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""

    def __init__(self):
        # {tenant_id: {user_id: WebSocket}}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str, user_id: str):
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = {}
        self.active_connections[tenant_id][user_id] = websocket

    def disconnect(self, tenant_id: str, user_id: str):
        if tenant_id in self.active_connections:
            self.active_connections[tenant_id].pop(user_id, None)

    async def send_work_order_update(
        self,
        tenant_id: str,
        work_order_id: str,
        update_type: str,
        data: Dict
    ):
        """Send work order update to all connected clients for this tenant"""
        if tenant_id in self.active_connections:
            message = {
                "type": "work_order_update",
                "work_order_id": work_order_id,
                "update_type": update_type,  # "stage_change", "agent_completed", "approval_required"
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }

            for websocket in self.active_connections[tenant_id].values():
                await websocket.send_json(message)

    async def send_agent_progress(
        self,
        tenant_id: str,
        work_order_id: str,
        agent_name: str,
        progress_pct: float,
        current_step: str
    ):
        """Send agent execution progress"""
        if tenant_id in self.active_connections:
            message = {
                "type": "agent_progress",
                "work_order_id": work_order_id,
                "agent_name": agent_name,
                "progress_pct": progress_pct,
                "current_step": current_step,
                "timestamp": datetime.utcnow().isoformat()
            }

            for websocket in self.active_connections[tenant_id].values():
                await websocket.send_json(message)

manager = ConnectionManager()

# FastAPI WebSocket endpoint
@router.websocket("/ws/{tenant_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    tenant_id: str,
    current_user: User = Depends(get_current_user_ws)
):
    await manager.connect(websocket, tenant_id, str(current_user.id))
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo heartbeat
            await websocket.send_json({"type": "heartbeat", "status": "ok"})
    except WebSocketDisconnect:
        manager.disconnect(tenant_id, str(current_user.id))
```

---

## Technology Stack

### Backend

**Core Framework:**
- FastAPI 0.109+ (async web framework)
- Python 3.11+
- Uvicorn (ASGI server)

**Orchestration & AI:**
- LangGraph 0.2+ (agent orchestration)
- LangChain 0.3+ (agent tooling)
- OpenRouter API (multi-model LLM access)
- LangSmith (debugging & monitoring)

**Data Processing:**
- Pandas 2.1+ (Excel/CSV processing)
- Polars 0.20+ (faster alternative for large files)
- OpenPyXL 3.1+ (Excel workbook manipulation)
- python-magic (file type detection)

**Database & Caching:**
- PostgreSQL 15+ / Supabase (primary database)
- SQLAlchemy 2.0+ (ORM)
- Alembic 1.13+ (migrations)
- Redis 7.0+ (Celery broker + caching)

**Task Queue:**
- Celery 5.3+ (async agent execution)
- Redis (message broker)

**Vector Store:**
- ChromaDB 0.4+ (mapping memory, semantic search)

**Security & Auth:**
- JWT tokens (python-jose)
- bcrypt 4.1+ (password hashing)

**Testing:**
- pytest 7.4+
- pytest-asyncio
- pytest-cov

**Monitoring:**
- Sentry (error tracking)
- Loguru (logging)

### Frontend

**Core:**
- React 18+
- TypeScript 5.3+
- Vite 5+ (build tool)

**UI & Styling:**
- Tailwind CSS 3.4+
- Headless UI (accessible components)

**State & Routing:**
- React Router 6+
- React Context (auth, work orders)
- React Query (server state, optional)

**API & WebSocket:**
- Axios 1.6+ (HTTP client)
- Native WebSocket API

**Testing:**
- Jest 29+
- React Testing Library

### Infrastructure

**Database:**
- Supabase PostgreSQL (hosted)

**Caching:**
- Redis (self-hosted or Redis Cloud)

**File Storage:**
- Local filesystem (initial)
- AWS S3 / MinIO (future)

**Deployment:**
- Docker (containerization, future)
- Railway / Render / Fly.io (backend)
- Vercel / Netlify (frontend)

---

## Security & Compliance

### Data Security

1. **Encryption:**
   - TLS 1.3 for all API traffic
   - At-rest encryption for database (Supabase default)
   - File uploads encrypted in transit

2. **Access Control:**
   - JWT token authentication
   - Role-based permissions (admin, cfo, controller, treasurer, analyst)
   - Tenant isolation (row-level security in PostgreSQL)
   - Approval authority checks

3. **Audit Trail:**
   - Immutable audit log (append-only table)
   - Full dataset lineage (input → processing → output)
   - Approval history with timestamps and rationale
   - Policy version tracking

4. **Spreadsheet Risk Mitigation:**
   - Workbook Auditor scans all uploads
   - Macros stripped by default
   - External links flagged
   - High-risk workbooks quarantined

### Compliance Features

1. **Policy-as-Code:**
   - Materiality thresholds enforced by Guardrail
   - SoD violations detected
   - Treasury limits validated
   - Disclosure gates applied

2. **Evidence Bundles:**
   - ZIP exports with artifacts, logs, policies
   - Disclosure checklists
   - Reconciliation support

3. **Retention:**
   - Dataset versions retained per policy (e.g., 7 years)
   - Audit logs immutable and archived

---

## Performance & Scalability

### Performance Targets

- **Ingestion latency**: ≤10 min per 100MB file
- **Mapping reuse**: ≥90% after first cycle
- **Agent execution**: Cash Commander ≤5 min, Portfolio Allocator ≤10 min
- **Real-time updates**: <1 sec WebSocket latency

### Scalability Strategy

1. **Horizontal Scaling:**
   - Stateless FastAPI instances (load balanced)
   - Celery workers auto-scale based on queue depth
   - PostgreSQL read replicas for reporting

2. **Vertical Scaling:**
   - Upgrade worker instance sizes for large files
   - Use Polars instead of Pandas for >1M rows

3. **Caching:**
   - Redis for mapping configs, policy packs
   - ChromaDB for mapping memory (persisted)

4. **Optimization:**
   - Incremental dataset processing (only changed rows)
   - Parallel agent execution where dependencies allow
   - Model selection (GPT-3.5 for routine, GPT-4 for complex)

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Set up LangGraph + OpenRouter integration
- Build File Intake Gateway (upload API + Workbook Auditor)
- Create Template Catalog backend
- Implement Dataset Versioning (PostgreSQL schema)
- Set up Celery + Redis task queue
- ChromaDB integration for mapping memory
- WebSocket server for real-time updates

### Phase 2: Core Agents (Weeks 5-8)
- Implement Work Order Graph (LangGraph StateGraph)
- Build Policy Engine + Guardrail agent
- Create Critic agent
- Implement 5 pilot agents:
  - Cash Commander
  - Close Copilot
  - Margin Mechanic
  - Forecast Factory
  - Payables Protector
- Build Compliance Scribe
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

## Success Criteria

### Technical SLOs

- **Ingestion**: ≤10 min per 100MB file
- **Mapping reuse**: ≥90% after first cycle
- **Day-3 close**: 2+ consecutive months
- **Bank rec**: T+1 coverage ≥99%
- **Duplicate detection**: ≥95% precision, ≥85% recall
- **Control logging**: 100% actions logged

### Agent Performance

- **Cash forecast MAPE**: ≤10% @ 2-week horizon
- **Revenue forecast MAPE**: ≤8% @ 90-day horizon
- **Margin bridge**: ≥95% GM delta explained
- **Auto-rec clearance**: ≥80%

### User Experience

- **Upload-to-insight**: ≤30 min median
- **Exception resolution**: ≤24 hrs P50
- **User satisfaction**: ≥4.0/5.0

---

## Future Enhancements

### Near-Term (6-12 months)

- Live connectors (QuickBooks, Xero, NetSuite) as optional supplements
- Advanced ML models for anomaly detection
- Multi-currency consolidation agent
- Email-based exception workflows

### Long-Term (12-24 months)

- Natural language query interface ("Show me DSO trend for top 10 customers")
- Auto-tuning of forecast models
- Integration with BI tools (Tableau, PowerBI)
- Mobile app for approvals
- Industry pack: Manufacturing (SIOP, inventory optimization)

---

## Appendix

### Template Catalog

**R2R:**
- TrialBalance.xlsx
- JE_Detail.csv
- FixedAssetsRegister.xlsx

**OTC:**
- AR_OpenItems.xlsx
- AR_AgedTrial.xlsx
- Cash_Receipts.xlsx

**PTP:**
- AP_OpenItems.xlsx
- Vendor_Master.xlsx
- Payments_Executed.csv

**Treasury:**
- BankStatement_BAI2/CSV.txt
- Debt_Schedule.xlsx
- FX_Rates.csv
- Hedge_Positions.xlsx

**Retail:**
- POS_Sales.csv
- Inventory_Snap.xlsx
- Promo_Calendar.xlsx
- Vendor_Terms_Rebates.xlsx

**Energy:**
- Production_Volumes.xlsx
- SCADA_Export.csv
- Turnaround_Schedule.xlsx
- Emissions_Ledger.xlsx

### Error Codes

- `E1001` MissingRequiredColumn
- `E1010` PeriodMismatch
- `E1020` UnbalancedTrialBalance
- `E2010` DuplicateInvoiceSuspected
- `E3010` PolicyBreach_PositivePay
- `E4010` MappingDriftDetected

---

**Document End**
