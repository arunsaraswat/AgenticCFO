"""Mapping configuration model for column mapping memory."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant
    from app.models.dataset import Dataset


class MappingConfig(Base):
    """
    Mapping configuration model for storing column mapping memory.

    Stores learned mappings from source column names to standardized template columns.
    Uses ChromaDB for semantic similarity search to suggest mappings for new files.

    Attributes:
        id: Primary key
        tenant_id: Foreign key to tenant
        template_type: Template type (TrialBalance, AP_OpenItems, POS_Sales, etc.)
        column_mappings: JSONB mapping source columns to template columns
        date_formats: JSONB with date format patterns
        validation_rules: JSONB with custom validation rules
        use_count: Number of times this mapping has been reused
        last_used_at: Last time this mapping was applied
        created_at: Timestamp when mapping was created
        updated_at: Timestamp when mapping was last updated

    Relationships:
        tenant: Tenant that owns this mapping
        datasets: Datasets that use this mapping configuration

    Example column_mappings:
        {
            "Account Number": "account_code",
            "Account Description": "account_name",
            "Debit Balance": "debit_amount",
            "Credit Balance": "credit_amount"
        }

    Example date_formats:
        {
            "date_column": "period_end_date",
            "format": "%m/%d/%Y",
            "timezone": "UTC"
        }
    """

    __tablename__ = "mapping_configs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    template_type = Column(String(100), nullable=False, index=True)
    column_mappings = Column(JSONB, nullable=False, default=dict)
    date_formats = Column(JSONB, nullable=False, default=dict)
    validation_rules = Column(JSONB, nullable=False, default=dict)
    use_count = Column(Integer, nullable=False, default=0)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("Tenant")
    datasets = relationship("Dataset", back_populates="mapping_config")

    def __repr__(self) -> str:
        """String representation of MappingConfig."""
        return f"<MappingConfig(id={self.id}, template_type={self.template_type}, use_count={self.use_count})>"
