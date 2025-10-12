"""User profile API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.user import UserProfileResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> UserProfileResponse:
    """
    Get current user's profile information.

    This is a protected endpoint that requires authentication.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User profile information
    """
    return UserProfileResponse.model_validate(current_user)
