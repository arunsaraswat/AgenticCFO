"""Dependency injection for FastAPI routes."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.user import User


def get_db_session() -> Session:
    """
    Get database session dependency.

    Yields:
        Database session
    """
    return Depends(get_db)


def get_authenticated_user() -> User:
    """
    Get authenticated user dependency.

    Returns:
        Current authenticated user
    """
    return Depends(get_current_active_user)
