"""File upload model for tracking uploaded files."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant
    from app.models.dataset import Dataset


class FileUpload(Base):
    """
    File upload model for tracking uploaded files.

    Tracks all files uploaded to the platform, including Excel, CSV, and other formats.
    Each file is scanned for security risks and analyzed by the Workbook Auditor agent.

    Attributes:
        id: Primary key
        tenant_id: Foreign key to tenant
        filename: Original filename
        file_path: Storage path for uploaded file
        file_hash: SHA-256 hash for deduplication and integrity
        file_size_bytes: File size in bytes
        mime_type: MIME type of uploaded file
        upload_channel: How file was uploaded (web, sftp, email)
        workbook_risk_score: Risk score from Workbook Auditor (0.0-1.0)
        security_scan_results: JSONB with virus scan and security check results
        status: Upload status (pending, processing, completed, failed)
        error_message: Error message if upload failed
        uploaded_by_user_id: User who uploaded the file
        created_at: Timestamp when file was uploaded

    Relationships:
        tenant: Tenant that owns this file
        datasets: Datasets created from this file
    """

    __tablename__ = "file_uploads"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(500), nullable=False)
    file_path = Column(Text, nullable=False)
    file_hash = Column(String(64), nullable=False, index=True)  # SHA-256
    file_size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=True)
    upload_channel = Column(String(50), nullable=False, default="web")  # web, sftp, email
    workbook_risk_score = Column(Float, nullable=True)  # 0.0-1.0
    security_scan_results = Column(JSONB, nullable=True, default=dict)
    status = Column(String(50), nullable=False, default="pending", index=True)  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="file_uploads")
    datasets = relationship("Dataset", back_populates="file_upload", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """String representation of FileUpload."""
        return f"<FileUpload(id={self.id}, filename={self.filename}, status={self.status})>"
