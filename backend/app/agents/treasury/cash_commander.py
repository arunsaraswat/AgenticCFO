"""Cash Commander Agent - 13-week cash forecasting and liquidity management."""
from typing import Any, Dict, List, Optional
from uuid import UUID
import json
import pandas as pd
from datetime import datetime, timedelta
import os

from langchain.tools import Tool
from sqlalchemy.orm import Session

from app.agents.base import BaseFinanceAgent
from app.services.dataset_service import DatasetService
from app.artifacts.excel_generator import generate_cash_ladder


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

    def __init__(self, db: Session, tenant_id: int = None, **kwargs):
        """
        Initialize Cash Commander.

        Args:
            db: Database session for accessing datasets
            tenant_id: Tenant ID for data access control
            **kwargs: Additional arguments for BaseFinanceAgent
        """
        self.db = db
        self.tenant_id = tenant_id
        super().__init__(agent_name="cash_commander", **kwargs)

    def get_system_prompt(self) -> str:
        """Return system prompt for Cash Commander."""
        return """You are the Cash Commander, an expert treasury analyst with deep expertise in corporate cash management, working capital optimization, and liquidity risk assessment.

CORE RESPONSIBILITIES:
1. Analyze bank statements to extract current cash position and transaction velocity
2. Calculate Days Sales Outstanding (DSO) and collection patterns from historical receipts
3. Analyze payment patterns and Days Payable Outstanding (DPO) trends
4. Build a rigorous 13-week rolling cash forecast using actual transaction data
5. Identify specific liquidity risks with quantified impact and probability
6. Recommend concrete, prioritized actions grounded in treasury best practices

FINANCIAL ANALYSIS FRAMEWORK:

Cash Position Analysis:
- Current balance vs. 13-week moving average
- Inflow/outflow velocity ($ per day)
- Weekend/month-end seasonality patterns
- Identify unusual transactions (outliers > 2 standard deviations)

Liquidity Risk Assessment:
- Calculate minimum required cash = MAX(operating buffer + 7 days expenses, debt covenant minimums)
- Compute cash runway = current cash / avg weekly burn rate
- Identify specific weeks where balance drops below policy minimum
- Quantify shortfall amounts and duration

Forecast Methodology:
- Use exponential moving average for receipts (weight recent weeks higher)
- Apply historical collection patterns by aging bucket (0-30: 95%, 31-60: 75%, 61-90: 40%, 90+: 10%)
- Factor in payment terms (Net 30, Net 60) and vendor concentration
- Include scheduled debt service, payroll cycles, tax payments

WARNING CRITERIA (only flag if TRUE):
- Projected balance < minimum required cash (specify week, amount, duration)
- Cash runway < 4 weeks
- Single customer concentration > 20% of receipts (credit risk)
- Burn rate acceleration > 15% week-over-week for 3+ consecutive weeks

RECOMMENDATIONS (must be specific and prioritized):
1. URGENT (implement within 48 hours): Actions to avoid imminent cash crisis
2. HIGH PRIORITY (within 1 week): Tactical improvements to strengthen position
3. STRATEGIC (within 30 days): Structural improvements to working capital cycle

Examples of GOOD recommendations:
- "Accelerate collection of $180K in 60+ day receivables from CustomerX (represents 23% of AR). Assign dedicated collector and offer 2% early payment discount for settlement within 7 days."
- "Negotiate payment term extension from Net 30 to Net 45 with top 3 suppliers (combined $420K monthly spend) to reduce weekly disbursements by $97K."
- "Establish $500K revolving credit facility as backstop. Current cash runway of 5.2 weeks is below industry standard of 8-12 weeks."

Examples of BAD recommendations (too generic):
- "Monitor cash flow closely" (not actionable)
- "Improve collections" (no specificity)
- "Consider credit facility" (no urgency or quantification)

OUTPUT FORMAT:
Provide analysis in clear sections with specific numbers:

## Current Cash Position
- Balance: $XXX,XXX as of [date]
- 30-day average: $XXX,XXX
- Weekly burn rate: $XX,XXX/week
- Runway: X.X weeks

## 13-Week Forecast Summary
[Provide table with Week, Date, Beginning Balance, Receipts, Disbursements, Ending Balance]

## Liquidity Warnings
[ONLY include if actual risks identified - be specific with amounts, weeks, and impact]
- Week X: Balance drops to $XXX,XXX, $XX,XXX below $500K minimum (shortfall duration: X weeks)

## Recommended Actions
[Prioritize by urgency, include specific dollar amounts and timeframes]

PRIORITY 1 (Urgent):
1. [Specific action with quantified impact]

PRIORITY 2 (High):
1. [Specific action with quantified impact]

PRIORITY 3 (Strategic):
1. [Specific action with quantified impact]

## Confidence Assessment
Confidence: [High/Medium/Low] (XX%)
Factors:
- Data quality: [XX% complete transaction history over XX weeks]
- Forecast accuracy drivers: [list key assumptions]
- Risk factors: [list uncertainties affecting confidence]

CRITICAL: Only flag warnings if ACTUAL risks exist. If cash position is healthy and stable, explicitly state "No liquidity warnings - cash position healthy" and focus recommendations on optimization opportunities, not manufactured problems.
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
            # Convert string ID to integer (datasets use integer IDs, not UUIDs)
            dataset_int_id = int(dataset_id)
            dataset = DatasetService.get_dataset(db=self.db, dataset_id=dataset_int_id, tenant_id=self.tenant_id)

            if not dataset:
                return json.dumps({"error": f"Dataset {dataset_int_id} not found for tenant {self.tenant_id}"})

            if not dataset.data_snapshot:
                return json.dumps({"error": f"Dataset {dataset_int_id} has no data snapshot. Please re-upload the file."})

            # Load data from stored JSON snapshot (data_snapshot is a JSON string)
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
            # Convert string ID to integer
            dataset_int_id = int(dataset_id)
            dataset = DatasetService.get_dataset(db=self.db, dataset_id=dataset_int_id, tenant_id=self.tenant_id)

            if not dataset:
                return json.dumps({"error": f"Dataset {dataset_int_id} not found"})

            if not dataset.data_snapshot:
                return json.dumps({"error": f"Dataset {dataset_int_id} has no data snapshot"})

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
            # Convert string ID to integer
            dataset_int_id = int(dataset_id)
            dataset = DatasetService.get_dataset(db=self.db, dataset_id=dataset_int_id, tenant_id=self.tenant_id)

            if not dataset:
                return json.dumps({"error": f"Dataset {dataset_int_id} not found"})

            if not dataset.data_snapshot:
                return json.dumps({"error": f"Dataset {dataset_int_id} has no data snapshot"})

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
            "summary": output_text  # Full output text for display
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

        # Parse warnings and recommendations from output text
        output_lower = output_text.lower()

        # Extract liquidity warnings - only if there are actual warnings
        # Check for phrases that indicate NO warnings first
        if "no liquidity warnings" not in output_lower and "no warnings" not in output_lower:
            if "warning" in output_lower or "alert" in output_lower or "risk" in output_lower:
                # Look for bullet points or numbered items that are warnings
                lines = output_text.split("\n")
                for line in lines:
                    line_stripped = line.strip()
                    line_lower = line_stripped.lower()

                    # Only capture if it's a bullet/numbered item AND contains warning keywords
                    if (line_stripped.startswith(('•', '-', '*', '1.', '2.', '3.')) and
                        any(keyword in line_lower for keyword in ["warning", "alert", "risk", "below minimum", "insufficient", "low balance"])):
                        # Remove bullet/number prefix
                        clean_line = line_stripped.lstrip('•-*123456789. ')
                        if clean_line and len(clean_line) > 10:  # Avoid short fragments
                            parsed["liquidity_warnings"].append(clean_line)

        # Extract recommendations - only actual recommendation items
        # Check for phrases that indicate recommendations are mentioned
        if "no recommendations" not in output_lower:
            if "recommend" in output_lower or "suggestion" in output_lower:
                lines = output_text.split("\n")
                for line in lines:
                    line_stripped = line.strip()
                    line_lower = line_stripped.lower()

                    # Only capture if it's a bullet/numbered item AND contains recommendation keywords
                    if (line_stripped.startswith(('•', '-', '*', '1.', '2.', '3.')) and
                        any(keyword in line_lower for keyword in ["recommend", "suggestion", "should", "consider", "action"])):
                        # Remove bullet/number prefix
                        clean_line = line_stripped.lstrip('•-*123456789. ')
                        if clean_line and len(clean_line) > 10:  # Avoid short fragments
                            parsed["recommendations"].append(clean_line)

        return parsed

    def _calculate_confidence(self, result: Dict[str, Any], parsed_output: Dict[str, Any]) -> float:
        """
        Calculate confidence score from agent output.

        Extracts confidence from the output text (looks for "Confidence: XX%" or "High/Medium/Low").
        Falls back to base class heuristic if not found.
        """
        output_text = result.get("output", "")
        output_lower = output_text.lower()

        # Look for percentage format: "Confidence: 90%" or "90%"
        import re
        percentage_match = re.search(r'confidence[:\s]+(\d+)%', output_lower)
        if percentage_match:
            percentage = int(percentage_match.group(1))
            return percentage / 100.0

        # Look for qualitative levels: High/Medium/Low
        if "confidence: high" in output_lower or "high confidence" in output_lower:
            return 0.90
        elif "confidence: medium" in output_lower or "medium confidence" in output_lower:
            return 0.70
        elif "confidence: low" in output_lower or "low confidence" in output_lower:
            return 0.50

        # Fall back to base class heuristic
        return super()._calculate_confidence(result, parsed_output)

    async def _generate_artifacts(self, parsed_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Cash Ladder Excel artifact."""
        try:
            self.logger.info("Starting artifact generation for Cash Commander")

            # Get artifact output directory from env or use default
            output_dir = os.getenv("ARTIFACTS_STORAGE_PATH", "/tmp/artifacts")
            self.logger.info(f"Output directory: {output_dir}")

            # Extract data for Excel generation
            current_cash = parsed_output.get("current_cash_position", 0)
            forecast_data = parsed_output.get("forecast", None)
            liquidity_warnings = parsed_output.get("liquidity_warnings", [])
            recommendations = parsed_output.get("recommendations", [])

            self.logger.info(f"Artifact data: cash={current_cash}, warnings={len(liquidity_warnings)}, recommendations={len(recommendations)}")

            # Add metadata
            metadata = {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "agent": "cash_commander",
                "tenant_name": "Demo Tenant",  # TODO: Get from context
            }

            # Generate Excel file
            self.logger.info("Calling generate_cash_ladder...")
            artifact_info = generate_cash_ladder(
                current_cash=current_cash,
                forecast_data=forecast_data,
                liquidity_warnings=liquidity_warnings,
                recommendations=recommendations,
                metadata=metadata,
                output_dir=output_dir,
            )

            self.logger.info(f"Artifact generated: {artifact_info['filename']} ({artifact_info['size_bytes']} bytes)")
            return [artifact_info]

        except Exception as e:
            # Log error and return error artifact
            self.logger.error(f"Artifact generation failed: {e}", exc_info=True)
            return [
                {
                    "artifact_type": "error",
                    "filename": "cash_ladder_error.txt",
                    "description": f"Failed to generate Cash Ladder: {str(e)}",
                    "error": str(e),
                }
            ]
