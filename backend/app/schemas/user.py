"""User-related Pydantic schemas."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base user schema with common attributes.

    Attributes:
        email: User email
        full_name: User's full name
    """

    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., description="User's full name")


class UserResponse(UserBase):
    """
    User response schema.

    Attributes:
        id: User ID
        is_active: Whether user is active
        created_at: Account creation timestamp
    """

    id: int = Field(..., description="User ID")
    is_active: bool = Field(..., description="User active status")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True


class UserProfileResponse(UserResponse):
    """
    Extended user profile response.

    Attributes:
        updated_at: Last update timestamp
        is_superuser: Whether user has admin privileges
    """

    updated_at: datetime = Field(..., description="Last update timestamp")
    is_superuser: bool = Field(..., description="Admin privileges status")

    class Config:
        from_attributes = True


class DashboardData(BaseModel):
    """
    Dashboard data schema.

    Attributes:
        user: User information
        stats: Dashboard statistics
        message: Welcome message
    """

    user: UserResponse
    stats: dict = Field(default_factory=dict, description="Dashboard statistics")
    message: str = Field(..., description="Welcome message")
