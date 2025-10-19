"""Artifact schemas for API requests and responses."""
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class ArtifactBase(BaseModel):
    """Base artifact schema with common attributes."""

    artifact_type: str = Field(..., description="Type of artifact (excel, pdf, word, json)")
    artifact_name: str = Field(..., description="Human-readable name")
    artifact_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class ArtifactCreate(ArtifactBase):
    """Schema for creating a new artifact."""

    work_order_id: int = Field(..., description="Work order that generated this artifact")
    file_path: str = Field(..., description="Storage path for artifact file")
    checksum_sha256: str = Field(..., min_length=64, max_length=64, description="SHA-256 checksum")
    file_size_bytes: int = Field(..., gt=0, description="File size in bytes")
    mime_type: Optional[str] = Field(None, max_length=100, description="MIME type")
    generated_by_agent: Optional[str] = Field(None, description="Agent that generated this artifact")


class ArtifactResponse(ArtifactBase):
    """Schema for artifact responses."""

    id: int = Field(..., description="Artifact ID")
    work_order_id: int = Field(..., description="Work order ID")
    file_path: str = Field(..., description="Storage path")
    checksum_sha256: str = Field(..., description="SHA-256 checksum")
    file_size_bytes: int = Field(..., description="File size in bytes")
    mime_type: Optional[str] = None
    generated_by_agent: Optional[str] = None
    created_at: datetime = Field(..., description="Timestamp when artifact was created")

    model_config = ConfigDict(from_attributes=True)
