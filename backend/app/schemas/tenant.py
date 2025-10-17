"""Tenant schemas for API requests and responses."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TenantBase(BaseModel):
    """Base tenant schema with common attributes."""

    name: str = Field(..., min_length=1, max_length=255, description="Tenant organization name")
    slug: str = Field(..., min_length=1, max_length=100, description="URL-friendly identifier")
    settings: dict = Field(default_factory=dict, description="Flexible tenant configuration")
    is_active: bool = Field(default=True, description="Whether tenant account is active")


class TenantCreate(TenantBase):
    """Schema for creating a new tenant."""

    pass


class TenantUpdate(BaseModel):
    """Schema for updating a tenant."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    settings: Optional[dict] = None
    is_active: Optional[bool] = None


class TenantResponse(TenantBase):
    """Schema for tenant responses."""

    id: int = Field(..., description="Tenant ID")
    created_at: datetime = Field(..., description="Timestamp when tenant was created")
    updated_at: datetime = Field(..., description="Timestamp when tenant was last updated")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
