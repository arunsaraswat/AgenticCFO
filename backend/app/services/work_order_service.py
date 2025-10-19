"""Work order service for executing agents and managing work order lifecycle."""
import hashlib
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.agents.treasury.cash_commander import CashCommanderAgent
from app.core.config import settings
from app.models.artifact import Artifact
from app.models.dataset import Dataset
from app.models.work_order import WorkOrder
from app.schemas.artifact import ArtifactCreate


class WorkOrderService:
    """Service for managing work order execution and lifecycle."""

    @staticmethod
    def create_work_order(
        db: Session,
        tenant_id: int,
        objective: str,
        input_datasets: List[int],
        created_by_user_id: int,
        policy_refs: Optional[List[str]] = None,
    ) -> WorkOrder:
        """
        Create a new work order.

        Args:
            db: Database session
            tenant_id: Tenant ID
            objective: Work order objective
            input_datasets: List of dataset IDs
            created_by_user_id: User ID who created the work order
            policy_refs: Optional policy references

        Returns:
            Created work order
        """
        work_order = WorkOrder(
            tenant_id=tenant_id,
            objective=objective,
            input_datasets=input_datasets,
            policy_refs=policy_refs or [],
            created_by_user_id=created_by_user_id,
            status="pending",
            progress_percentage=0,
            execution_log=[
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "event": "work_order_created",
                    "details": {
                        "objective": objective,
                        "dataset_count": len(input_datasets),
                    },
                }
            ],
        )

        db.add(work_order)
        db.commit()
        db.refresh(work_order)

        return work_order

    @staticmethod
    async def execute_cash_commander(
        db: Session,
        work_order_id: int,
        tenant_id: int,
    ) -> WorkOrder:
        """
        Execute Cash Commander agent for a work order.

        Args:
            db: Database session
            work_order_id: Work order ID to execute
            tenant_id: Tenant ID for access control

        Returns:
            Updated work order with execution results

        Raises:
            ValueError: If work order not found or invalid state
            Exception: If agent execution fails
        """
        # Fetch work order
        work_order = db.query(WorkOrder).filter(
            WorkOrder.id == work_order_id,
            WorkOrder.tenant_id == tenant_id
        ).first()

        if not work_order:
            raise ValueError(f"Work order {work_order_id} not found")

        if work_order.status not in ["pending", "failed"]:
            raise ValueError(f"Work order {work_order_id} is in '{work_order.status}' state and cannot be executed")

        try:
            # Update status to processing
            work_order.status = "processing"
            work_order.progress_percentage = 10
            work_order.current_agent = "cash_commander"
            work_order.execution_log.append({
                "timestamp": datetime.utcnow().isoformat(),
                "event": "execution_started",
                "agent": "cash_commander",
            })
            db.commit()

            # Get input datasets
            dataset_ids = work_order.input_datasets
            if not dataset_ids:
                raise ValueError("Work order has no input datasets")

            # Fetch datasets from database
            datasets = db.query(Dataset).filter(
                Dataset.id.in_(dataset_ids),
                Dataset.tenant_id == tenant_id
            ).all()

            if not datasets:
                raise ValueError(f"No datasets found for IDs: {dataset_ids}")

            # Prepare inputs for agent
            # For now, assume first dataset is bank statement
            # In future, detect template_type
            inputs = {}
            for dataset in datasets:
                template_type = dataset.template_type.lower() if dataset.template_type else "unknown"

                if "bank" in template_type or "statement" in template_type:
                    inputs["bank_statement_id"] = str(dataset.id)
                elif "ar" in template_type or "receivable" in template_type:
                    inputs["ar_aging_id"] = str(dataset.id)
                elif "ap" in template_type or "payable" in template_type:
                    inputs["ap_aging_id"] = str(dataset.id)

            if not inputs.get("bank_statement_id"):
                # Use first dataset as bank statement if no bank statement detected
                inputs["bank_statement_id"] = str(datasets[0].id)

            # Policy constraints (use defaults for now)
            policy_constraints = {
                "min_cash_balance": 500000.0,
                "forecast_weeks": 13,
            }

            # Update progress
            work_order.progress_percentage = 30
            db.commit()

            # Initialize and execute agent
            start_time = time.time()
            agent = CashCommanderAgent(db=db, tenant_id=tenant_id)

            result = await agent.execute(
                inputs=inputs,
                policy_constraints=policy_constraints
            )

            execution_time = time.time() - start_time

            # Update progress
            work_order.progress_percentage = 70
            db.commit()

            # Save agent output to work order
            work_order.agent_outputs = {
                "cash_commander": {
                    "output": result.output,
                    "confidence_score": result.confidence_score,
                    "reasoning_trace": result.reasoning_trace,
                    "execution_time": result.execution_time,
                    "metadata": result.metadata,
                }
            }

            # Save artifacts to database
            artifact_records = []
            for artifact_data in result.artifacts:
                artifact_path = artifact_data.get("file_path")
                if not artifact_path or not os.path.exists(artifact_path):
                    continue

                # Calculate checksum (or use provided one)
                checksum = artifact_data.get("checksum_sha256")
                if not checksum:
                    with open(artifact_path, "rb") as f:
                        file_content = f.read()
                        checksum = hashlib.sha256(file_content).hexdigest()
                        file_size = len(file_content)
                else:
                    file_size = artifact_data.get("size_bytes", os.path.getsize(artifact_path))

                # Create artifact record
                artifact = Artifact(
                    work_order_id=work_order.id,
                    artifact_type=artifact_data.get("artifact_type", "excel"),
                    artifact_name=artifact_data.get("filename", artifact_data.get("artifact_name", "Cash_Ladder.xlsx")),
                    file_path=artifact_path,
                    checksum_sha256=checksum,
                    file_size_bytes=file_size,
                    mime_type=artifact_data.get("mime_type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                    artifact_metadata=artifact_data.get("metadata", {}),
                    generated_by_agent="cash_commander",
                )
                db.add(artifact)
                artifact_records.append({
                    "artifact_type": artifact.artifact_type,
                    "artifact_name": artifact.artifact_name,
                    "file_size_bytes": artifact.file_size_bytes,
                })

            db.commit()

            # Update work order to completed
            work_order.status = "completed"
            work_order.progress_percentage = 100
            work_order.current_agent = None
            work_order.total_cost_usd = result.metadata.get("cost_usd", 0.0)
            work_order.execution_time_seconds = execution_time
            work_order.completed_at = datetime.utcnow()
            work_order.artifacts = artifact_records
            work_order.execution_log.append({
                "timestamp": datetime.utcnow().isoformat(),
                "event": "execution_completed",
                "agent": "cash_commander",
                "execution_time": execution_time,
                "artifact_count": len(artifact_records),
            })

            db.commit()
            db.refresh(work_order)

            return work_order

        except Exception as e:
            # Update work order to failed state
            work_order.status = "failed"
            work_order.current_agent = None
            work_order.error_message = str(e)
            work_order.execution_log.append({
                "timestamp": datetime.utcnow().isoformat(),
                "event": "execution_failed",
                "agent": "cash_commander",
                "error": str(e),
            })
            db.commit()
            db.refresh(work_order)

            raise

    @staticmethod
    def get_work_order(
        db: Session,
        work_order_id: int,
        tenant_id: int,
    ) -> Optional[WorkOrder]:
        """
        Get a work order by ID.

        Args:
            db: Database session
            work_order_id: Work order ID
            tenant_id: Tenant ID for access control

        Returns:
            Work order if found, None otherwise
        """
        return db.query(WorkOrder).filter(
            WorkOrder.id == work_order_id,
            WorkOrder.tenant_id == tenant_id
        ).first()

    @staticmethod
    def list_work_orders(
        db: Session,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[WorkOrder]:
        """
        List work orders for a tenant.

        Args:
            db: Database session
            tenant_id: Tenant ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of work orders
        """
        return db.query(WorkOrder).filter(
            WorkOrder.tenant_id == tenant_id
        ).order_by(WorkOrder.created_at.desc()).offset(skip).limit(limit).all()
