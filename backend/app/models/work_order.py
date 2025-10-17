"""Work order model for LangGraph orchestration."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant
    from app.models.artifact import Artifact
    from app.models.audit_event import AuditEvent


class WorkOrder(Base):
    """
    Work order model for LangGraph orchestration.

    Each uploaded file triggers a Work Order that flows through the LangGraph StateGraph.
    The Work Order tracks inputs, agent outputs, guardrail checks, approval gates, and artifacts.

    Attributes:
        id: Primary key
        tenant_id: Foreign key to tenant
        objective: High-level objective (e.g., "13-week cash forecast")
        input_datasets: JSONB array of dataset IDs used as inputs
        policy_refs: JSONB array of policy pack references
        agent_outputs: JSONB dict mapping agent names to their outputs
        guardrail_checks: JSONB array of guardrail check results
        approval_gates: JSONB array of approval gate records
        artifacts: JSONB array of artifact references
        execution_log: JSONB array of state transitions (immutable, append-only)
        status: Current status (pending, routing, processing, approval_required, completed, failed)
        progress_percentage: Overall progress (0-100)
        current_agent: Currently executing agent name
        error_message: Error message if work order failed
        total_cost_usd: Total cost of LLM API calls
        execution_time_seconds: Total execution time
        created_by_user_id: User who created the work order
        created_at: Timestamp when work order was created
        updated_at: Timestamp when work order was last updated
        completed_at: Timestamp when work order completed

    Relationships:
        tenant: Tenant that owns this work order
        artifacts: Generated artifacts
        audit_events: Related audit events

    Example input_datasets:
        [1, 2, 3]  # Array of dataset IDs

    Example policy_refs:
        ["Policy_Pack_V3#Treasury", "Policy_Pack_V3#Materiality"]

    Example agent_outputs:
        {
            "cash_commander": {
                "output": {...},
                "confidence_score": 0.92,
                "reasoning_trace": [...],
                "execution_time": 45.2,
                "cost_usd": 0.15
            }
        }

    Example guardrail_checks:
        [
            {
                "check_name": "minimum_cash_balance",
                "status": "failed",
                "severity": "critical",
                "reason": "Cash balance $450K below policy minimum $500K"
            }
        ]

    Example execution_log:
        [
            {"timestamp": "2025-01-15T10:00:00Z", "event": "work_order_created", "details": {...}},
            {"timestamp": "2025-01-15T10:01:00Z", "event": "routing_completed", "details": {...}},
            {"timestamp": "2025-01-15T10:02:00Z", "event": "agent_started", "agent": "cash_commander"}
        ]
    """

    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    objective = Column(String(500), nullable=False)
    input_datasets = Column(JSONB, nullable=False, default=list)
    policy_refs = Column(JSONB, nullable=False, default=list)
    agent_outputs = Column(JSONB, nullable=False, default=dict)
    guardrail_checks = Column(JSONB, nullable=False, default=list)
    approval_gates = Column(JSONB, nullable=False, default=list)
    artifacts = Column(JSONB, nullable=False, default=list)
    execution_log = Column(JSONB, nullable=False, default=list)
    status = Column(String(50), nullable=False, default="pending", index=True)
    progress_percentage = Column(Integer, nullable=False, default=0)
    current_agent = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    total_cost_usd = Column(Float, nullable=False, default=0.0)
    execution_time_seconds = Column(Float, nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="work_orders")
    artifacts = relationship("Artifact", back_populates="work_order", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="work_order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """String representation of WorkOrder."""
        return f"<WorkOrder(id={self.id}, objective={self.objective}, status={self.status})>"
