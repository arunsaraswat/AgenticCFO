"""Test work order artifact generation end-to-end."""
import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.work_order import WorkOrder
from app.models.artifact import Artifact

async def test_check_work_order_artifacts():
    """Check if work orders have generated artifacts."""
    db: Session = SessionLocal()

    try:
        # Get the most recent work order
        work_orders = db.query(WorkOrder).order_by(WorkOrder.id.desc()).limit(5).all()

        print(f"\n📊 Recent Work Orders ({len(work_orders)}):\n")

        for wo in work_orders:
            print(f"Work Order #{wo.id}")
            print(f"  Status: {wo.status}")
            print(f"  Objective: {wo.objective}")
            print(f"  Created: {wo.created_at}")

            # Check agent outputs
            if wo.agent_outputs:
                print(f"  Agent Outputs: {list(wo.agent_outputs.keys())}")

                # Check if Cash Commander ran
                if "cash_commander" in wo.agent_outputs:
                    cc_output = wo.agent_outputs["cash_commander"]["output"]
                    print(f"  Cash Commander Output Keys: {list(cc_output.keys())}")
                    print(f"    - current_cash_position: {cc_output.get('current_cash_position')}")
                    print(f"    - liquidity_warnings: {len(cc_output.get('liquidity_warnings', []))} warnings")
                    print(f"    - recommendations: {len(cc_output.get('recommendations', []))} recommendations")

            # Check artifacts in JSONB field
            if wo.artifacts:
                print(f"  Artifacts (JSONB): {len(wo.artifacts)} items")
                for artifact_info in wo.artifacts:
                    print(f"    - {artifact_info.get('artifact_name')} ({artifact_info.get('artifact_type')})")

            # Check artifacts in database table
            db_artifacts = db.query(Artifact).filter(Artifact.work_order_id == wo.id).all()
            if db_artifacts:
                print(f"  Artifacts (DB): {len(db_artifacts)} records")
                for artifact in db_artifacts:
                    print(f"    - {artifact.artifact_name} ({artifact.artifact_type})")
                    print(f"      Path: {artifact.file_path}")
                    print(f"      Size: {artifact.file_size_bytes:,} bytes")
                    print(f"      Checksum: {artifact.checksum_sha256[:16]}...")
            else:
                print(f"  Artifacts (DB): 0 records")

            print()

    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_check_work_order_artifacts())
