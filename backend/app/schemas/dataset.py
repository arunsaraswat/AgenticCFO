"""Dataset schemas for API requests and responses."""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class DatasetBase(BaseModel):
    """Base dataset schema with common attributes."""

    template_type: str = Field(..., min_length=1, max_length=100, description="Template type")
    entity: Optional[str] = Field(None, max_length=255, description="Entity/company name")
    period_start: Optional[date] = Field(None, description="Period start date")
    period_end: Optional[date] = Field(None, description="Period end date")


class DatasetCreate(DatasetBase):
    """Schema for creating a new dataset."""

    file_upload_id: int = Field(..., description="Foreign key to file upload")
    data_hash: str = Field(..., min_length=64, max_length=64, description="SHA-256 hash of data")
    mapping_config_id: Optional[int] = None
    row_count: Optional[int] = Field(None, gt=0, description="Number of rows")
    column_count: Optional[int] = Field(None, gt=0, description="Number of columns")
    dataset_metadata: dict = Field(default_factory=dict, description="Additional metadata")
    data_snapshot: Optional[str] = Field(None, description="JSON snapshot of parsed data (DataFrame.to_json())")


class DatasetUpdate(BaseModel):
    """Schema for updating a dataset."""

    dq_status: Optional[str] = Field(None, description="Data quality status")
    dq_results: Optional[dict] = None
    dataset_metadata: Optional[dict] = None


class DatasetResponse(DatasetBase):
    """Schema for dataset responses."""

    id: int = Field(..., description="Dataset ID")
    tenant_id: int = Field(..., description="Tenant ID")
    file_upload_id: int = Field(..., description="File upload ID")
    version: int = Field(..., description="Version number")
    data_hash: str = Field(..., description="SHA-256 hash")
    mapping_config_id: Optional[int] = None
    dq_status: str = Field(..., description="Data quality status")
    dq_results: Optional[dict] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    dataset_metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(..., description="Timestamp when dataset was created")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
