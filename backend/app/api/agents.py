"""API endpoints for agent execution."""
from typing import Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.agents.treasury.cash_commander import CashCommanderAgent

router = APIRouter(prefix="/agents", tags=["Agents"])


class ExecuteCashCommanderRequest(BaseModel):
    """Request model for executing Cash Commander."""
    bank_statement_id: UUID
    ar_aging_id: UUID | None = None
    ap_aging_id: UUID | None = None
    min_cash_balance: float = 500000.0
    forecast_weeks: int = 13


class ExecuteCashCommanderResponse(BaseModel):
    """Response model for Cash Commander execution."""
    agent_name: str
    output: Dict[str, Any]
    confidence_score: float
    artifacts: list[Dict[str, Any]]
    reasoning_trace: list[str]
    execution_time: float
    metadata: Dict[str, Any]


@router.post("/cash-commander/execute", response_model=ExecuteCashCommanderResponse)
async def execute_cash_commander(
    request: ExecuteCashCommanderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExecuteCashCommanderResponse:
    """
    Execute Cash Commander agent for 13-week cash forecasting.

    This endpoint:
    1. Initializes the Cash Commander agent
    2. Loads the specified datasets (bank statement, AR, AP)
    3. Executes cash flow analysis and forecasting
    4. Returns structured output with artifacts

    Args:
        request: Execution parameters including dataset IDs
        current_user: Authenticated user
        db: Database session

    Returns:
        Agent output with forecast, warnings, and artifacts
    """
    try:
        # Initialize agent
        agent = CashCommanderAgent(db=db)

        # Prepare inputs
        inputs = {
            "bank_statement_id": str(request.bank_statement_id),
        }

        if request.ar_aging_id:
            inputs["ar_aging_id"] = str(request.ar_aging_id)

        if request.ap_aging_id:
            inputs["ap_aging_id"] = str(request.ap_aging_id)

        # Policy constraints
        policy_constraints = {
            "min_cash_balance": request.min_cash_balance,
            "forecast_weeks": request.forecast_weeks,
        }

        # Execute agent
        result = await agent.execute(
            inputs=inputs,
            policy_constraints=policy_constraints
        )

        return ExecuteCashCommanderResponse(
            agent_name=result.agent_name,
            output=result.output,
            confidence_score=result.confidence_score,
            artifacts=result.artifacts,
            reasoning_trace=result.reasoning_trace,
            execution_time=result.execution_time,
            metadata=result.metadata
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )


@router.get("/cash-commander/status")
async def cash_commander_status(
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Check Cash Commander agent status and configuration.

    Returns:
        Agent status and model configuration
    """
    from app.agents.llm_config import LLMConfig

    return {
        "agent_name": "cash_commander",
        "status": "ready",
        "model": LLMConfig.get_model_for_agent("cash_commander"),
        "capabilities": [
            "13-week cash forecasting",
            "Bank statement analysis",
            "AR/AP projection",
            "Liquidity warning detection",
            "Cash Ladder generation"
        ]
    }
