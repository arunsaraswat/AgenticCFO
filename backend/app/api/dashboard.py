"""Dashboard API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.user import DashboardData, UserResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardData)
async def get_dashboard_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> DashboardData:
    """
    Get dashboard data for current user.

    This is a protected endpoint that requires authentication.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        Dashboard data including user info and stats
    """
    # Example dashboard statistics - replace with real data
    stats = {
        "total_items": 42,
        "active_projects": 5,
        "completed_tasks": 28,
        "pending_tasks": 14
    }

    return DashboardData(
        user=UserResponse.model_validate(current_user),
        stats=stats,
        message=f"Welcome back, {current_user.full_name}!"
    )
