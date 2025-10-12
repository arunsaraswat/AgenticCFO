"""Authentication-related Pydantic schemas."""
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """
    Login request schema.

    Attributes:
        email: User email
        password: User password
    """

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class LoginResponse(BaseModel):
    """
    Login response schema.

    Attributes:
        access_token: JWT access token
        token_type: Token type (always "bearer")
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class RegisterRequest(BaseModel):
    """
    User registration request schema.

    Attributes:
        email: User email
        password: User password
        full_name: User's full name
    """

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    full_name: str = Field(..., min_length=2, description="User's full name")


class RegisterResponse(BaseModel):
    """
    User registration response schema.

    Attributes:
        id: User ID
        email: User email
        full_name: User's full name
        message: Success message
    """

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    full_name: str = Field(..., description="User's full name")
    message: str = Field(default="User registered successfully")
