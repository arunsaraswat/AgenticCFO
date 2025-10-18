"""Dataset model for versioned data storage."""
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant
    from app.models.file_upload import FileUpload
    from app.models.mapping_config import MappingConfig


class Dataset(Base):
    """
    Dataset model for versioned data storage.

    Each uploaded file creates an immutable versioned dataset. Never modified,
    only new versions are created. Supports full lineage tracking.

    Attributes:
        id: Primary key
        tenant_id: Foreign key to tenant
        file_upload_id: Foreign key to original file upload
        template_type: Template type (TrialBalance, AP_OpenItems, etc.)
        entity: Entity/company name this data belongs to
        period_start: Period start date
        period_end: Period end date
        version: Version number for this dataset
        data_hash: SHA-256 hash of processed data
        mapping_config_id: Foreign key to mapping configuration used
        dq_status: Data quality validation status
        dq_results: JSONB with data quality validation results
        row_count: Number of rows in dataset
        column_count: Number of columns in dataset
        dataset_metadata: JSONB with additional metadata
        created_at: Timestamp when dataset was created

    Relationships:
        tenant: Tenant that owns this dataset
        file_upload: Original file upload
        mapping_config: Mapping configuration used to create this dataset

    Unique Constraint:
        (tenant_id, template_type, entity, period_start, version)
        Ensures immutability and proper versioning
    """

    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    file_upload_id = Column(Integer, ForeignKey("file_uploads.id", ondelete="CASCADE"), nullable=False, index=True)
    template_type = Column(String(100), nullable=False, index=True)
    entity = Column(String(255), nullable=True, index=True)
    period_start = Column(Date, nullable=True, index=True)
    period_end = Column(Date, nullable=True, index=True)
    version = Column(Integer, nullable=False, default=1)
    data_hash = Column(String(64), nullable=False, index=True)  # SHA-256
    mapping_config_id = Column(Integer, ForeignKey("mapping_configs.id", ondelete="SET NULL"), nullable=True)
    dq_status = Column(String(50), nullable=False, default="pending")  # pending, passed, failed, warning
    dq_results = Column(JSONB, nullable=True, default=dict)
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)
    dataset_metadata = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Unique constraint for versioning
    __table_args__ = (
        UniqueConstraint("tenant_id", "template_type", "entity", "period_start", "version", name="uq_dataset_version"),
    )

    # Relationships (Tenant relationship commented out to avoid circular import)
    # tenant = relationship("Tenant", back_populates="datasets")
    file_upload = relationship("FileUpload", back_populates="datasets")
    mapping_config = relationship("MappingConfig", back_populates="datasets")

    def __repr__(self) -> str:
        """String representation of Dataset."""
        return f"<Dataset(id={self.id}, template_type={self.template_type}, entity={self.entity}, version={self.version})>"
