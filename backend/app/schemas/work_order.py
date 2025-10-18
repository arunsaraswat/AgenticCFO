"""Work order schemas."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class WorkOrderBase(BaseModel):
    """Base work order schema."""
    objective: str
    input_datasets: Optional[List[int]] = []
    policy_refs: Optional[List[str]] = []


class WorkOrderCreate(WorkOrderBase):
    """Schema for creating a work order."""
    pass


class WorkOrderResponse(WorkOrderBase):
    """Schema for work order response."""
    id: int
    tenant_id: int
    status: str
    progress_percentage: int
    current_agent: Optional[str] = None
    agent_outputs: Optional[Dict[str, Any]] = {}
    guardrail_checks: Optional[List[Dict[str, Any]]] = []
    approval_gates: Optional[List[Dict[str, Any]]] = []
    artifacts: Optional[List[Dict[str, Any]]] = []
    execution_log: Optional[List[Dict[str, Any]]] = []
    error_message: Optional[str] = None
    total_cost_usd: float = 0.0
    execution_time_seconds: Optional[float] = None
    created_by_user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
