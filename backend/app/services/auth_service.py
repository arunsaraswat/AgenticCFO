"""Authentication service with business logic."""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import verify_password, get_password_hash, create_access_token


class AuthService:
    """
    Authentication service for user management and authentication.

    Handles user registration, login, and validation logic.
    """

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            db: Database session
            email: User email

        Returns:
            User object or None if not found
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            User object if authenticated, None otherwise
        """
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def register_user(db: Session, user_data: RegisterRequest) -> User:
        """
        Register a new user.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Created user object

        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = AuthService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def login_user(db: Session, login_data: LoginRequest) -> str:
        """
        Login user and generate JWT token.

        Args:
            db: Database session
            login_data: Login credentials

        Returns:
            JWT access token

        Raises:
            HTTPException: If credentials are invalid
        """
        user = AuthService.authenticate_user(db, login_data.email, login_data.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )

        # Create access token with user email as subject
        access_token = create_access_token(data={"sub": user.email})
        return access_token
