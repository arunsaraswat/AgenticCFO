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


async def get_authenticated_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get authenticated user dependency.

    This is a convenience wrapper that returns the authenticated user directly.

    Args:
        current_user: Current authenticated user from get_current_active_user

    Returns:
        Current authenticated user with tenant_id available
    """
    return current_user


# Alias for compatibility
get_current_user = get_authenticated_user
