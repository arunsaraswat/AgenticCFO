"""
Unit test for data_snapshot field in Dataset model.

Tests that data_snapshot is correctly saved and retrieved.
"""
import pandas as pd
import pytest
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate
from app.services.dataset_service import DatasetService


def test_dataset_create_with_data_snapshot(db: Session, test_tenant):
    """Test that create_dataset properly stores data_snapshot."""
    # Create sample DataFrame
    df = pd.DataFrame({
        "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "Amount": [100.0, 200.0, 300.0],
        "Description": ["Test 1", "Test 2", "Test 3"]
    })

    # Convert to JSON
    data_json = df.to_json(orient="records")

    # Create dataset with data_snapshot
    dataset_data = DatasetCreate(
        template_type="BankStatement",
        entity="Test Corp",
        period_start=None,
        period_end=None,
        file_upload_id=1,  # Mock file upload ID
        data_hash="a" * 64,  # Mock hash
        mapping_config_id=None,
        row_count=3,
        column_count=3,
        dataset_metadata={"test": True},
        data_snapshot=data_json  # THIS IS THE CRITICAL FIELD
    )

    # Call create_dataset
    dataset = DatasetService.create_dataset(db, test_tenant.id, dataset_data)

    # Assertions
    assert dataset.id is not None
    assert dataset.data_snapshot is not None, "data_snapshot should be saved to database"
    assert len(dataset.data_snapshot) > 0, "data_snapshot should contain data"

    # Verify data can be loaded back
    loaded_df = pd.read_json(dataset.data_snapshot)
    assert len(loaded_df) == 3, "Should have 3 rows"
    assert list(loaded_df.columns) == ["Date", "Amount", "Description"]

    print(f"✅ Dataset {dataset.id} created with data_snapshot ({len(dataset.data_snapshot)} chars)")


def test_dataset_data_snapshot_persists_across_sessions(db: Session, test_tenant):
    """Test that data_snapshot survives database commits and queries."""
    df = pd.DataFrame({
        "Col1": [1, 2, 3],
        "Col2": ["a", "b", "c"]
    })
    data_json = df.to_json(orient="records")

    # Create dataset
    dataset_data = DatasetCreate(
        template_type="TestTemplate",
        entity=None,
        period_start=None,
        period_end=None,
        file_upload_id=1,
        data_hash="b" * 64,
        mapping_config_id=None,
        row_count=3,
        column_count=2,
        dataset_metadata={},
        data_snapshot=data_json
    )

    created_dataset = DatasetService.create_dataset(db, test_tenant.id, dataset_data)
    dataset_id = created_dataset.id

    # Commit and clear session (simulating a new request)
    db.commit()
    db.expunge_all()

    # Query dataset in new "session"
    retrieved_dataset = DatasetService.get_dataset(db, dataset_id, test_tenant.id)

    # Verify data_snapshot persisted
    assert retrieved_dataset is not None
    assert retrieved_dataset.data_snapshot is not None
    assert retrieved_dataset.data_snapshot == data_json

    # Verify it can be parsed
    reloaded_df = pd.read_json(retrieved_dataset.data_snapshot)
    assert len(reloaded_df) == 3
    assert list(reloaded_df.columns) == ["Col1", "Col2"]

    print(f"✅ data_snapshot persisted across sessions for dataset {dataset_id}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
