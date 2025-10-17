"""Audit event model for immutable audit trail."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant
    from app.models.work_order import WorkOrder


class AuditEvent(Base):
    """
    Audit event model for immutable audit trail.

    Append-only log of all significant events in the system. Never updated or deleted.
    Provides complete audit trail for compliance and debugging.

    Attributes:
        id: Primary key
        tenant_id: Foreign key to tenant
        work_order_id: Foreign key to work order (optional)
        event_type: Type of event (file_upload, agent_execution, approval_granted, etc.)
        event_category: Category (intake, orchestration, agent, control, output, auth)
        user_id: User who triggered the event (optional)
        details: JSONB with event-specific details
        ip_address: IP address of request (for web events)
        user_agent: User agent string (for web events)
        timestamp: Timestamp when event occurred (indexed for queries)

    Relationships:
        tenant: Tenant that owns this audit event
        work_order: Related work order (optional)

    Event Types:
        - file_upload: File uploaded to system
        - dataset_created: New dataset version created
        - work_order_created: New work order initiated
        - agent_started: Agent began execution
        - agent_completed: Agent finished execution
        - guardrail_failed: Guardrail check failed
        - approval_requested: Approval gate triggered
        - approval_granted: Human approved continuation
        - approval_denied: Human rejected continuation
        - artifact_generated: Output artifact created
        - policy_violation: Policy rule violated
        - user_login: User authenticated
        - user_logout: User logged out

    Example details:
        {
            "agent_name": "cash_commander",
            "confidence_score": 0.92,
            "execution_time_seconds": 45.2,
            "cost_usd": 0.15,
            "reasoning_summary": "Analyzed 3 bank statements, identified $2.5M in upcoming disbursements"
        }
    """

    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    event_category = Column(String(50), nullable=False, index=True)  # intake, orchestration, agent, control, output, auth
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    details = Column(JSONB, nullable=False, default=dict)
    ip_address = Column(String(45), nullable=True)  # IPv6 max length
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="audit_events")
    work_order = relationship("WorkOrder", back_populates="audit_events")

    def __repr__(self) -> str:
        """String representation of AuditEvent."""
        return f"<AuditEvent(id={self.id}, type={self.event_type}, timestamp={self.timestamp})>"
