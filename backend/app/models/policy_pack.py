"""Policy pack model for policy-as-code enforcement."""
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant


class PolicyPack(Base):
    """
    Policy pack model for storing policy-as-code rules.

    Policy packs contain rules for materiality thresholds, segregation of duties,
    treasury limits, disclosure gates, and other compliance requirements.

    Attributes:
        id: Primary key
        tenant_id: Foreign key to tenant
        name: Policy pack name (e.g., "Policy_Pack_V3")
        version: Version number
        policy_data: JSONB containing all policy rules
        effective_from: Date when policy becomes effective
        effective_to: Date when policy expires (null = indefinite)
        is_active: Whether policy pack is currently active
        created_at: Timestamp when policy pack was created
        updated_at: Timestamp when policy pack was last updated

    Relationships:
        tenant: Tenant that owns this policy pack

    Example policy_data structure:
        {
            "treasury": {
                "minimum_cash_balance": 500000,
                "max_fx_exposure_pct": 0.15,
                "credit_line_buffer_days": 30
            },
            "materiality": {
                "variance_threshold_usd": 100000,
                "revenue_recognition_threshold_pct": 0.05
            },
            "segregation_of_duties": {
                "same_user_approval_forbidden": true,
                "payment_approval_limit_usd": 50000
            },
            "disclosure_gates": {
                "revenue_recognition_criteria": ["goods_delivered", "price_fixed", "collectability_probable"],
                "accrual_documentation_required": true
            }
        }
    """

    __tablename__ = "policy_packs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    policy_data = Column(JSONB, nullable=False, default=dict)
    effective_from = Column(Date, nullable=False, index=True)
    effective_to = Column(Date, nullable=True, index=True)
    is_active = Column(Integer, nullable=False, default=1)  # Using Integer for index compatibility
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships (Tenant relationship commented out to avoid circular import)
    # tenant = relationship("Tenant", back_populates="policy_packs")

    def __repr__(self) -> str:
        """String representation of PolicyPack."""
        return f"<PolicyPack(id={self.id}, name={self.name}, version={self.version}, is_active={self.is_active})>"
