"""Work order API endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.work_order import WorkOrder
from app.schemas.work_order import WorkOrderResponse, WorkOrderCreate

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.get("", response_model=List[WorkOrderResponse])
async def get_work_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> List[WorkOrderResponse]:
    """
    Get all work orders for the current user's tenant.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of work orders
    """
    work_orders = db.query(WorkOrder).filter(
        WorkOrder.tenant_id == current_user.tenant_id
    ).order_by(WorkOrder.created_at.desc()).offset(skip).limit(limit).all()

    return [WorkOrderResponse.model_validate(wo) for wo in work_orders]


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
async def get_work_order(
    work_order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> WorkOrderResponse:
    """
    Get a specific work order by ID.

    Args:
        work_order_id: Work order ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Work order details
    """
    work_order = db.query(WorkOrder).filter(
        WorkOrder.id == work_order_id,
        WorkOrder.tenant_id == current_user.tenant_id
    ).first()

    if not work_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work order not found"
        )

    return WorkOrderResponse.model_validate(work_order)


@router.post("", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_work_order(
    work_order_data: WorkOrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> WorkOrderResponse:
    """
    Create a new work order.

    Args:
        work_order_data: Work order creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created work order
    """
    work_order = WorkOrder(
        tenant_id=current_user.tenant_id,
        objective=work_order_data.objective,
        input_datasets=work_order_data.input_datasets or [],
        policy_refs=work_order_data.policy_refs or [],
        created_by_user_id=current_user.id,
        status="pending"
    )

    db.add(work_order)
    db.commit()
    db.refresh(work_order)

    return WorkOrderResponse.model_validate(work_order)
