"""Service layer for dataset operations."""
import asyncio
import hashlib
import json
from datetime import datetime
from typing import Optional

import pandas as pd
from sqlalchemy.orm import Session

from app.intake.column_mapper import ColumnMapper
from app.intake.dq_validator import DQValidator
from app.intake.file_parser import FileParser
from app.intake.template_detector import TemplateDetector
from app.models.dataset import Dataset
from app.models.mapping_config import MappingConfig
from app.schemas.dataset import DatasetCreate, DatasetUpdate


class DatasetService:
    """
    Service for managing datasets.

    Handles parsing, template detection, column mapping, and DQ validation.
    """

    @staticmethod
    def create_dataset(db: Session, tenant_id: int, dataset_data: DatasetCreate) -> Dataset:
        """
        Create a new dataset record.

        Args:
            db: Database session
            tenant_id: Tenant ID
            dataset_data: Dataset creation data

        Returns:
            Created Dataset instance
        """
        dataset = Dataset(
            tenant_id=tenant_id,
            file_upload_id=dataset_data.file_upload_id,
            template_type=dataset_data.template_type,
            entity=dataset_data.entity,
            period_start=dataset_data.period_start,
            period_end=dataset_data.period_end,
            version=1,  # Will be incremented if same dataset already exists
            data_hash=dataset_data.data_hash,
            mapping_config_id=dataset_data.mapping_config_id,
            dq_status="pending",
            row_count=dataset_data.row_count,
            column_count=dataset_data.column_count,
            dataset_metadata=dataset_data.dataset_metadata,
            created_at=datetime.utcnow(),
        )

        # Check for existing version and increment
        existing = (
            db.query(Dataset)
            .filter(
                Dataset.tenant_id == tenant_id,
                Dataset.template_type == dataset_data.template_type,
                Dataset.entity == dataset_data.entity,
                Dataset.period_start == dataset_data.period_start,
            )
            .order_by(Dataset.version.desc())
            .first()
        )

        if existing:
            dataset.version = existing.version + 1

        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        return dataset

    @staticmethod
    def get_dataset(db: Session, dataset_id: int, tenant_id: int) -> Optional[Dataset]:
        """
        Get dataset by ID.

        Args:
            db: Database session
            dataset_id: Dataset ID
            tenant_id: Tenant ID for filtering

        Returns:
            Dataset instance or None if not found
        """
        return (
            db.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.tenant_id == tenant_id)
            .first()
        )

    @staticmethod
    def update_dataset(
        db: Session, dataset_id: int, tenant_id: int, update_data: DatasetUpdate
    ) -> Optional[Dataset]:
        """
        Update dataset record.

        Args:
            db: Database session
            dataset_id: Dataset ID
            tenant_id: Tenant ID for filtering
            update_data: Update data

        Returns:
            Updated Dataset instance or None if not found
        """
        dataset = DatasetService.get_dataset(db, dataset_id, tenant_id)
        if not dataset:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(dataset, key, value)

        db.commit()
        db.refresh(dataset)
        return dataset

    @staticmethod
    def list_datasets(
        db: Session, tenant_id: int, skip: int = 0, limit: int = 100
    ) -> list[Dataset]:
        """
        List datasets for a tenant.

        Args:
            db: Database session
            tenant_id: Tenant ID for filtering
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Dataset instances
        """
        return (
            db.query(Dataset)
            .filter(Dataset.tenant_id == tenant_id)
            .order_by(Dataset.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    async def process_file_upload(
        db: Session, tenant_id: int, file_upload_id: int, file_path: str
    ) -> tuple[Optional[Dataset], dict]:
        """
        Process uploaded file into a dataset.

        Complete workflow:
        1. Parse file (Excel/CSV)
        2. Detect template type
        3. Map columns to standard schema
        4. Run DQ validation
        5. Create dataset record
        6. Store/reuse mapping configuration

        Args:
            db: Database session
            tenant_id: Tenant ID
            file_upload_id: File upload ID
            file_path: Path to uploaded file

        Returns:
            Tuple of (Dataset, processing_results_dict)
            Returns (None, error_dict) if processing fails
        """
        processing_results = {
            "success": False,
            "steps": {},
            "errors": [],
        }

        try:
            # Step 1: Parse file (CPU-intensive, run in thread pool)
            df = await asyncio.to_thread(FileParser.parse_file, file_path)
            processing_results["steps"]["parsing"] = {
                "status": "success",
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": df.columns.tolist(),
            }

            # Step 2: Detect template type (CPU-intensive, run in thread pool)
            template_type, confidence = await asyncio.to_thread(
                TemplateDetector.detect_from_dataframe, df
            )

            if not template_type:
                processing_results["errors"].append(
                    "Could not detect template type. Please ensure file has recognizable column headers."
                )
                return None, processing_results

            processing_results["steps"]["template_detection"] = {
                "status": "success",
                "template_type": template_type,
                "confidence": round(confidence, 3),
            }

            # Step 3: Map columns (run in thread pool)
            column_mappings = await asyncio.to_thread(
                ColumnMapper.map_columns, df.columns.tolist(), template_type
            )
            mapping_confidence = ColumnMapper.get_mapping_confidence(column_mappings)
            is_valid, missing_columns = ColumnMapper.validate_mappings(
                column_mappings, template_type
            )

            if not is_valid:
                processing_results["errors"].append(
                    f"Missing required columns: {', '.join(missing_columns)}"
                )
                processing_results["steps"]["column_mapping"] = {
                    "status": "failed",
                    "mappings": column_mappings,
                    "confidence": round(mapping_confidence, 3),
                    "missing_columns": missing_columns,
                }
                return None, processing_results

            processing_results["steps"]["column_mapping"] = {
                "status": "success",
                "mappings": column_mappings,
                "confidence": round(mapping_confidence, 3),
            }

            # Step 4: Run DQ validation (CPU-intensive, run in thread pool)
            dq_result = await asyncio.to_thread(
                DQValidator.validate_dataset, df, template_type, column_mappings
            )
            processing_results["steps"]["dq_validation"] = dq_result.to_dict()

            # Step 5: Calculate data hash (CPU-intensive for large datasets, run in thread pool)
            data_json = await asyncio.to_thread(df.to_json, orient="records")
            data_hash = hashlib.sha256(data_json.encode()).hexdigest()

            # Step 6: Store/reuse mapping configuration
            mapping_config = DatasetService._get_or_create_mapping_config(
                db, tenant_id, template_type, column_mappings
            )

            # Step 7: Create dataset record
            dataset_data = DatasetCreate(
                file_upload_id=file_upload_id,
                template_type=template_type,
                entity=None,  # TODO: Extract from file or metadata
                period_start=None,  # TODO: Extract from date columns
                period_end=None,  # TODO: Extract from date columns
                data_hash=data_hash,
                mapping_config_id=mapping_config.id if mapping_config else None,
                row_count=len(df),
                column_count=len(df.columns),
                dataset_metadata={
                    "template_confidence": confidence,
                    "mapping_confidence": mapping_confidence,
                    "column_mappings": column_mappings,
                    "source_columns": df.columns.tolist(),
                },
            )

            dataset = DatasetService.create_dataset(db, tenant_id, dataset_data)

            # Step 8: Update DQ status
            DatasetService.update_dataset(
                db,
                dataset.id,
                tenant_id,
                DatasetUpdate(
                    dq_status=dq_result.status,
                    dq_results=dq_result.to_dict(),
                ),
            )

            processing_results["success"] = True
            processing_results["dataset_id"] = dataset.id

            return dataset, processing_results

        except Exception as e:
            processing_results["errors"].append(f"Processing failed: {str(e)}")
            return None, processing_results

    @staticmethod
    def _get_or_create_mapping_config(
        db: Session, tenant_id: int, template_type: str, column_mappings: dict
    ) -> Optional[MappingConfig]:
        """
        Get existing mapping config or create new one.

        Reuses existing config if identical mapping exists (mapping memory).

        Args:
            db: Database session
            tenant_id: Tenant ID
            template_type: Template type
            column_mappings: Column mappings dict

        Returns:
            MappingConfig instance or None
        """
        # Convert mappings to JSON for comparison
        mappings_json = json.dumps(column_mappings, sort_keys=True)

        # Look for existing identical mapping
        existing = (
            db.query(MappingConfig)
            .filter(
                MappingConfig.tenant_id == tenant_id,
                MappingConfig.template_type == template_type,
            )
            .all()
        )

        for config in existing:
            if json.dumps(config.column_mappings, sort_keys=True) == mappings_json:
                # Found matching config, increment use count
                config.use_count += 1
                config.last_used_at = datetime.utcnow()
                db.commit()
                return config

        # Create new mapping config
        mapping_config = MappingConfig(
            tenant_id=tenant_id,
            template_type=template_type,
            column_mappings=column_mappings,
            date_formats={},  # TODO: Extract detected date formats
            validation_rules={},
            use_count=1,
            last_used_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.add(mapping_config)
        db.commit()
        db.refresh(mapping_config)
        return mapping_config
