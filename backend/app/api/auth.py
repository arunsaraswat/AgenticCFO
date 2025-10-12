"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
) -> RegisterResponse:
    """
    Register a new user.

    Args:
        user_data: User registration information
        db: Database session

    Returns:
        Created user information

    Raises:
        HTTPException: If email already exists (400)
    """
    user = AuthService.register_user(db, user_data)
    return RegisterResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        message="User registered successfully"
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> LoginResponse:
    """
    Login user and receive JWT token.

    Args:
        login_data: Login credentials
        db: Database session

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid (401) or user is inactive (400)
    """
    access_token = AuthService.login_user(db, login_data)
    return LoginResponse(access_token=access_token, token_type="bearer")
