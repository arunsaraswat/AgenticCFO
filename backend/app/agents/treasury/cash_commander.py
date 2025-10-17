"""Cash Commander Agent - 13-week cash forecasting and liquidity management."""
from typing import Any, Dict, List, Optional
from uuid import UUID
import json
import pandas as pd
from datetime import datetime, timedelta

from langchain.tools import Tool
from sqlalchemy.orm import Session

from app.agents.base import BaseFinanceAgent
from app.services.dataset_service import DatasetService


class CashCommanderAgent(BaseFinanceAgent):
    """
    Cash Commander Agent.

    Responsibilities:
    - Analyze bank statements to extract current cash position
    - Forecast 13-week cash flows from AR/AP aging
    - Identify liquidity risks and covenant warnings
    - Generate Cash Ladder artifact (Excel)

    Inputs:
    - Bank statement dataset (last 30-90 days)
    - AR open items dataset
    - AP open items dataset
    - Policy constraints (min cash balance, etc.)

    Outputs:
    - Current cash position
    - 13-week cash forecast (weekly buckets)
    - Liquidity warnings
    - Cash Ladder Excel artifact
    """

    def __init__(self, db: Session, **kwargs):
        """
        Initialize Cash Commander.

        Args:
            db: Database session for accessing datasets
            **kwargs: Additional arguments for BaseFinanceAgent
        """
        self.db = db
        self.dataset_service = DatasetService(db)
        super().__init__(agent_name="cash_commander", **kwargs)

    def get_system_prompt(self) -> str:
        """Return system prompt for Cash Commander."""
        return """You are the Cash Commander, an expert treasury agent specializing in cash forecasting and liquidity management.

Your responsibilities:
1. Analyze bank statements to determine current cash position
2. Project future cash flows from AR collections and AP payments
3. Build a 13-week rolling cash forecast
4. Identify liquidity risks (minimum cash balance violations, covenant breaches)
5. Recommend actions to maintain healthy liquidity

Key capabilities:
- Extract and analyze cash transactions from bank statements
- Calculate collection rates from AR aging (current vs overdue)
- Calculate payment timing from AP aging and payment terms
- Apply policy constraints (minimum cash balance, maximum drawdown)
- Flag high-risk scenarios requiring human approval

Output format:
- Current cash position (ending balance)
- Weekly cash forecast for 13 weeks (beginning balance, receipts, disbursements, ending balance)
- Liquidity warnings (if any)
- Recommended actions
- Confidence score (0.0-1.0)

Always explain your reasoning and show your calculations.
"""

    def get_default_tools(self) -> List[Tool]:
        """Return tools for Cash Commander."""
        return [
            Tool(
                name="load_bank_statement",
                func=self._load_bank_statement,
                description="Load bank statement data. Input: dataset_id (UUID string)"
            ),
            Tool(
                name="load_ar_aging",
                func=self._load_ar_aging,
                description="Load AR open items. Input: dataset_id (UUID string)"
            ),
            Tool(
                name="load_ap_aging",
                func=self._load_ap_aging,
                description="Load AP open items. Input: dataset_id (UUID string)"
            ),
            Tool(
                name="calculate_collection_rate",
                func=self._calculate_collection_rate,
                description="Calculate AR collection rate from historical data. Input: bank_statement_data (JSON string)"
            ),
        ]

    def _load_bank_statement(self, dataset_id: str) -> str:
        """Load bank statement dataset."""
        try:
            dataset_uuid = UUID(dataset_id)
            dataset = self.dataset_service.get_dataset(dataset_uuid)

            if not dataset:
                return json.dumps({"error": "Dataset not found"})

            # Load data from stored DataFrame
            df = pd.read_json(dataset.data_snapshot)

            # Return summary + last 10 transactions
            summary = {
                "total_rows": len(df),
                "ending_balance": float(df["Balance"].iloc[-1]) if "Balance" in df.columns else None,
                "date_range": {
                    "start": df["Date"].min() if "Date" in df.columns else None,
                    "end": df["Date"].max() if "Date" in df.columns else None,
                },
                "total_receipts": float(df["Credit"].sum()) if "Credit" in df.columns else 0,
                "total_disbursements": float(df["Debit"].sum()) if "Debit" in df.columns else 0,
                "recent_transactions": df.tail(10).to_dict(orient="records")
            }

            return json.dumps(summary, default=str)

        except Exception as e:
            return json.dumps({"error": str(e)})

    def _load_ar_aging(self, dataset_id: str) -> str:
        """Load AR aging dataset."""
        try:
            dataset_uuid = UUID(dataset_id)
            dataset = self.dataset_service.get_dataset(dataset_uuid)

            if not dataset:
                return json.dumps({"error": "Dataset not found"})

            df = pd.read_json(dataset.data_snapshot)

            summary = {
                "total_ar": float(df["Amount"].sum()) if "Amount" in df.columns else 0,
                "num_invoices": len(df),
                "overdue_ar": float(df[df["Status"] == "Overdue"]["Amount"].sum()) if "Status" in df.columns else 0,
                "current_ar": float(df[df["Status"] == "Current"]["Amount"].sum()) if "Status" in df.columns else 0,
                "invoices": df.to_dict(orient="records")
            }

            return json.dumps(summary, default=str)

        except Exception as e:
            return json.dumps({"error": str(e)})

    def _load_ap_aging(self, dataset_id: str) -> str:
        """Load AP aging dataset."""
        try:
            dataset_uuid = UUID(dataset_id)
            dataset = self.dataset_service.get_dataset(dataset_uuid)

            if not dataset:
                return json.dumps({"error": "Dataset not found"})

            df = pd.read_json(dataset.data_snapshot)

            summary = {
                "total_ap": float(df["Amount"].sum()) if "Amount" in df.columns else 0,
                "num_invoices": len(df),
                "due_this_week": float(df[df["Days_Until_Due"] <= 7]["Amount"].sum()) if "Days_Until_Due" in df.columns else 0,
                "invoices": df.to_dict(orient="records")
            }

            return json.dumps(summary, default=str)

        except Exception as e:
            return json.dumps({"error": str(e)})

    def _calculate_collection_rate(self, bank_statement_data: str) -> str:
        """Calculate AR collection rate from bank statement."""
        try:
            data = json.loads(bank_statement_data)
            total_receipts = data.get("total_receipts", 0)
            num_days = 30  # Assuming 30-day statement

            # Simple heuristic: daily collection rate
            daily_rate = total_receipts / num_days if num_days > 0 else 0

            return json.dumps({
                "daily_collection_rate": daily_rate,
                "weekly_collection_rate": daily_rate * 7,
                "monthly_collection_rate": daily_rate * 30
            })

        except Exception as e:
            return json.dumps({"error": str(e)})

    def _prepare_input(self, inputs: Dict[str, Any], policy_constraints: Optional[Dict[str, Any]]) -> str:
        """Format inputs for Cash Commander."""
        prompt_parts = [
            "# Cash Forecasting Task",
            "",
            "## Datasets Available"
        ]

        # Add dataset IDs
        if "bank_statement_id" in inputs:
            prompt_parts.append(f"- Bank Statement Dataset ID: {inputs['bank_statement_id']}")

        if "ar_aging_id" in inputs:
            prompt_parts.append(f"- AR Aging Dataset ID: {inputs['ar_aging_id']}")

        if "ap_aging_id" in inputs:
            prompt_parts.append(f"- AP Aging Dataset ID: {inputs['ap_aging_id']}")

        # Add policy constraints
        if policy_constraints:
            prompt_parts.extend([
                "",
                "## Policy Constraints",
                f"- Minimum Cash Balance: ${policy_constraints.get('min_cash_balance', 500000):,.2f}",
                f"- Forecast Horizon: {policy_constraints.get('forecast_weeks', 13)} weeks"
            ])

        prompt_parts.extend([
            "",
            "## Your Task",
            "1. Load the bank statement to determine current cash position",
            "2. Load AR aging to forecast cash receipts",
            "3. Load AP aging to forecast cash disbursements",
            "4. Build a 13-week rolling cash forecast",
            "5. Check for liquidity warnings (minimum balance violations)",
            "6. Provide recommendations",
            "",
            "Please proceed step by step and explain your reasoning."
        ])

        return "\n".join(prompt_parts)

    def _parse_output(self, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Cash Commander output."""
        output_text = raw_output.get("output", "")

        # For MVP, extract structured data from the agent's response
        # In production, you'd use function calling or structured output
        parsed = {
            "current_cash_position": None,
            "forecast": [],
            "liquidity_warnings": [],
            "recommendations": [],
            "summary": output_text[:500]  # First 500 chars
        }

        # Extract intermediate steps for more context
        steps = raw_output.get("intermediate_steps", [])
        for step in steps:
            if isinstance(step, tuple) and len(step) >= 2:
                action, observation = step[0], step[1]

                # Try to extract current cash from bank statement
                if action.tool == "load_bank_statement":
                    try:
                        data = json.loads(observation)
                        parsed["current_cash_position"] = data.get("ending_balance")
                    except:
                        pass

        return parsed

    async def _generate_artifacts(self, parsed_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Cash Ladder Excel artifact."""
        # For now, return placeholder
        # Will implement full Excel generation in next step
        return [
            {
                "artifact_type": "excel",
                "filename": "Cash_Ladder.xlsx",
                "description": "13-week cash forecast",
                "status": "pending_generation"
            }
        ]
