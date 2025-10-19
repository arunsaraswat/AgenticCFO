"""File upload schemas for API requests and responses."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FileUploadBase(BaseModel):
    """Base file upload schema with common attributes."""

    filename: str = Field(..., min_length=1, max_length=500, description="Original filename")
    upload_channel: str = Field(default="web", description="How file was uploaded")


class FileUploadCreate(FileUploadBase):
    """Schema for creating a new file upload."""

    file_path: str = Field(..., description="Storage path for uploaded file")
    file_hash: str = Field(..., min_length=64, max_length=64, description="SHA-256 hash")
    file_size_bytes: int = Field(..., gt=0, description="File size in bytes")
    mime_type: Optional[str] = Field(None, max_length=100, description="MIME type")
    uploaded_by_user_id: Optional[int] = None


class FileUploadUpdate(BaseModel):
    """Schema for updating a file upload."""

    status: Optional[str] = Field(None, description="Upload status")
    workbook_risk_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Risk score 0.0-1.0")
    security_scan_results: Optional[dict] = None
    error_message: Optional[str] = None


class FileUploadResponse(FileUploadBase):
    """Schema for file upload responses."""

    id: int = Field(..., description="File upload ID")
    tenant_id: int = Field(..., description="Tenant ID")
    file_hash: str = Field(..., description="SHA-256 hash")
    file_size_bytes: int = Field(..., description="File size in bytes")
    mime_type: Optional[str] = None
    workbook_risk_score: Optional[float] = None
    security_scan_results: Optional[dict] = None
    status: str = Field(..., description="Upload status")
    error_message: Optional[str] = None
    uploaded_by_user_id: Optional[int] = None
    created_at: datetime = Field(..., description="Timestamp when file was uploaded")
    work_order_id: Optional[int] = Field(None, description="Work order ID if auto-created")
    dataset_id: Optional[int] = Field(None, description="Dataset ID if created")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
