"""Tenant model for multi-tenancy support."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.file_upload import FileUpload
    from app.models.dataset import Dataset
    from app.models.work_order import WorkOrder
    from app.models.policy_pack import PolicyPack
    from app.models.audit_event import AuditEvent


class Tenant(Base):
    """
    Tenant model for multi-tenancy support.

    Each tenant represents a separate organization using the Agentic CFO platform.
    All data is isolated by tenant_id to ensure data security and privacy.

    Attributes:
        id: Primary key
        name: Tenant organization name
        slug: URL-friendly identifier
        settings: JSONB column for flexible tenant configuration
        is_active: Whether tenant account is active
        created_at: Timestamp when tenant was created
        updated_at: Timestamp when tenant was last updated

    Relationships:
        users: Users belonging to this tenant
        file_uploads: File uploads for this tenant
        datasets: Datasets for this tenant
        work_orders: Work orders for this tenant
        policy_packs: Policy packs for this tenant
        audit_events: Audit events for this tenant
    """

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    settings = Column(JSONB, nullable=False, default=dict)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    file_uploads = relationship("FileUpload", back_populates="tenant", cascade="all, delete-orphan")
    datasets = relationship("Dataset", back_populates="tenant", cascade="all, delete-orphan")
    work_orders = relationship("WorkOrder", back_populates="tenant", cascade="all, delete-orphan")
    policy_packs = relationship("PolicyPack", back_populates="tenant", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="tenant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """String representation of Tenant."""
        return f"<Tenant(id={self.id}, slug={self.slug}, name={self.name})>"
