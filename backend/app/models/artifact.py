"""Artifact model for tracking generated outputs."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.work_order import WorkOrder


class Artifact(Base):
    """
    Artifact model for tracking generated outputs.

    Artifacts are the final deliverables from work orders: Excel files, PDFs, Word documents.
    Each artifact has a SHA-256 checksum for integrity verification.

    Attributes:
        id: Primary key
        work_order_id: Foreign key to work order
        artifact_type: Type of artifact (excel, pdf, word, json)
        artifact_name: Human-readable name
        file_path: Storage path for artifact file
        checksum_sha256: SHA-256 checksum for integrity verification
        file_size_bytes: File size in bytes
        mime_type: MIME type of artifact
        artifact_metadata: JSONB with additional metadata
        generated_by_agent: Agent that generated this artifact
        created_at: Timestamp when artifact was created

    Relationships:
        work_order: Work order that generated this artifact

    Example artifact types:
        - excel: Cash_Ladder.xlsx, GM_Bridge_BU_SKU.xlsx, Portfolio_Ranked.xlsx
        - pdf: Liquidity_Warnings.pdf, Covenant_Report.pdf
        - word: Investment_Memos.docx
        - json: structured data exports

    Example metadata:
        {
            "sheet_names": ["Cash Ladder", "Summary", "Assumptions"],
            "row_count": 156,
            "chart_count": 3,
            "confidence_score": 0.92
        }
    """

    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    artifact_type = Column(String(50), nullable=False, index=True)  # excel, pdf, word, json
    artifact_name = Column(String(500), nullable=False)
    file_path = Column(Text, nullable=False)
    checksum_sha256 = Column(String(64), nullable=False, index=True)
    file_size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=True)
    artifact_metadata = Column(JSONB, nullable=False, default=dict)
    generated_by_agent = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    work_order = relationship("WorkOrder", back_populates="artifacts")

    def __repr__(self) -> str:
        """String representation of Artifact."""
        return f"<Artifact(id={self.id}, type={self.artifact_type}, name={self.artifact_name})>"
