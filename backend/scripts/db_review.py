#!/usr/bin/env python3
"""
Database Schema and Relationship Review Script

This script performs comprehensive validation of the database schema,
foreign key relationships, data integrity, and best practices.

Usage:
    python backend/scripts/db_review.py

    Or via slash command:
    /db-review
"""

import sys
import os
from typing import Dict, List, Tuple, Any
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Import ALL models first (critical for FK resolution)
from app.models import (
    Tenant, User, FileUpload, Dataset, MappingConfig,
    PolicyPack, WorkOrder, AuditEvent, Artifact
)
from app.db.session import engine
from app.db.base import Base
from sqlalchemy import inspect, text, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError


class DatabaseReviewer:
    """Comprehensive database schema and relationship validator."""

    def __init__(self):
        self.engine = engine
        self.inspector = inspect(self.engine)
        self.metadata = Base.metadata
        self.results = {
            'errors': [],
            'warnings': [],
            'info': [],
            'stats': {}
        }

    def run_all_checks(self):
        """Run all database validation checks."""
        print("=" * 80)
        print("DATABASE SCHEMA & RELATIONSHIP REVIEW")
        print("=" * 80)
        print()

        # Phase 1: Model Registration
        print("Phase 1: Checking Model Registration...")
        self.check_model_registration()

        # Phase 2: Schema Validation
        print("\nPhase 2: Validating Database Schema...")
        self.validate_schema()

        # Phase 3: Foreign Key Relationships
        print("\nPhase 3: Verifying Foreign Key Relationships...")
        self.verify_foreign_keys()

        # Phase 4: Data Integrity
        print("\nPhase 4: Checking Data Integrity...")
        self.check_data_integrity()

        # Phase 5: Best Practices
        print("\nPhase 5: Validating Best Practices...")
        self.check_best_practices()

        # Phase 6: Performance Analysis
        print("\nPhase 6: Analyzing Performance...")
        self.analyze_performance()

        # Print Report
        print()
        self.print_report()

        # Return exit code
        return 0 if not self.results['errors'] else 1

    def check_model_registration(self):
        """Verify all models are properly registered with SQLAlchemy."""
        print("  Checking SQLAlchemy model registration...")

        registered_models = list(Base.registry.mappers)
        model_count = len(registered_models)

        self.results['stats']['registered_models'] = model_count
        self.results['info'].append(f"✓ {model_count} models registered with SQLAlchemy")

        # List all registered models
        for mapper in registered_models:
            model_name = mapper.class_.__name__
            table_name = mapper.mapped_table.name
            print(f"    ✓ {model_name:20s} -> {table_name}")

        # Check for expected models
        expected_models = {
            'Tenant', 'User', 'FileUpload', 'Dataset', 'MappingConfig',
            'PolicyPack', 'WorkOrder', 'AuditEvent', 'Artifact'
        }

        registered_model_names = {mapper.class_.__name__ for mapper in registered_models}
        missing_models = expected_models - registered_model_names

        if missing_models:
            self.results['errors'].append(
                f"Missing expected models: {', '.join(missing_models)}"
            )
        else:
            self.results['info'].append("✓ All expected models are registered")

    def validate_schema(self):
        """Validate database schema matches model definitions."""
        print("  Validating schema consistency...")

        db_tables = set(self.inspector.get_table_names())
        model_tables = {mapper.mapped_table.name for mapper in Base.registry.mappers}

        self.results['stats']['database_tables'] = len(db_tables)
        self.results['stats']['model_tables'] = len(model_tables)

        # Check for missing tables
        missing_tables = model_tables - db_tables
        if missing_tables:
            for table in missing_tables:
                self.results['errors'].append(f"Table defined in model but missing in DB: {table}")

        # Check for orphaned tables
        orphaned_tables = db_tables - model_tables - {'alembic_version'}
        if orphaned_tables:
            for table in orphaned_tables:
                self.results['warnings'].append(f"Table exists in DB but not defined in models: {table}")

        if not missing_tables and not orphaned_tables:
            print(f"    ✓ All {len(model_tables)} model tables exist in database")
            self.results['info'].append("✓ Schema is consistent between models and database")

    def verify_foreign_keys(self):
        """Verify all foreign key relationships are valid."""
        print("  Verifying foreign key constraints...")

        fk_count = 0
        fk_issues = []

        for mapper in Base.registry.mappers:
            table = mapper.mapped_table
            model_name = mapper.class_.__name__

            if table.foreign_keys:
                for fk in table.foreign_keys:
                    fk_count += 1
                    parent_col = fk.parent.name
                    target_table = fk.column.table.name
                    target_col = fk.column.name

                    # Check if target table exists
                    if target_table not in self.inspector.get_table_names():
                        fk_issues.append(
                            f"{model_name}.{parent_col} -> {target_table}.{target_col} "
                            f"(target table '{target_table}' does not exist)"
                        )
                    else:
                        # Check if target column exists
                        target_columns = [col['name'] for col in self.inspector.get_columns(target_table)]
                        if target_col not in target_columns:
                            fk_issues.append(
                                f"{model_name}.{parent_col} -> {target_table}.{target_col} "
                                f"(target column '{target_col}' does not exist)"
                            )

        self.results['stats']['foreign_keys'] = fk_count

        if fk_issues:
            for issue in fk_issues:
                self.results['errors'].append(f"FK validation failed: {issue}")
        else:
            print(f"    ✓ All {fk_count} foreign key relationships are valid")
            self.results['info'].append(f"✓ {fk_count} foreign key constraints validated")

    def check_data_integrity(self):
        """Check for data integrity issues."""
        print("  Checking data integrity constraints...")

        with self.engine.connect() as conn:
            # Check for orphaned records (FK violations)
            integrity_checks = [
                # Users with invalid tenant_id
                ("users", "tenant_id", "tenants", "id"),
                # FileUploads with invalid tenant_id or user_id
                ("file_uploads", "tenant_id", "tenants", "id"),
                ("file_uploads", "uploaded_by_user_id", "users", "id"),
                # Datasets with invalid references
                ("datasets", "tenant_id", "tenants", "id"),
                ("datasets", "file_upload_id", "file_uploads", "id"),
                # WorkOrders with invalid references
                ("work_orders", "tenant_id", "tenants", "id"),
                ("work_orders", "created_by_user_id", "users", "id"),
                # Artifacts with invalid work_order_id
                ("artifacts", "work_order_id", "work_orders", "id"),
            ]

            orphaned_count = 0
            for child_table, child_col, parent_table, parent_col in integrity_checks:
                # Skip if child column allows NULL
                columns = self.inspector.get_columns(child_table)
                col_info = next((c for c in columns if c['name'] == child_col), None)

                if col_info and col_info.get('nullable', True):
                    # Column allows NULL, so we only check non-NULL values
                    query = text(f"""
                        SELECT COUNT(*) FROM {child_table}
                        WHERE {child_col} IS NOT NULL
                          AND {child_col} NOT IN (SELECT {parent_col} FROM {parent_table})
                    """)
                else:
                    query = text(f"""
                        SELECT COUNT(*) FROM {child_table}
                        WHERE {child_col} NOT IN (SELECT {parent_col} FROM {parent_table})
                    """)

                try:
                    result = conn.execute(query)
                    count = result.scalar()

                    if count > 0:
                        orphaned_count += count
                        self.results['errors'].append(
                            f"Found {count} orphaned records in {child_table}.{child_col} "
                            f"(referencing non-existent {parent_table}.{parent_col})"
                        )
                except Exception as e:
                    self.results['warnings'].append(
                        f"Could not check integrity for {child_table}.{child_col}: {str(e)}"
                    )

            if orphaned_count == 0:
                print(f"    ✓ No orphaned records found")
                self.results['info'].append("✓ All foreign key references are valid (no orphans)")

    def check_best_practices(self):
        """Validate database best practices."""
        print("  Validating best practices...")

        # Check 1: All tenant_id columns should be indexed
        tenant_tables = ['users', 'file_uploads', 'datasets', 'mapping_configs',
                        'policy_packs', 'work_orders', 'audit_events']

        missing_indexes = []
        for table in tenant_tables:
            indexes = self.inspector.get_indexes(table)
            tenant_id_indexed = any('tenant_id' in idx['column_names'] for idx in indexes)

            if not tenant_id_indexed:
                missing_indexes.append(f"{table}.tenant_id")

        if missing_indexes:
            for col in missing_indexes:
                self.results['warnings'].append(f"Missing index on {col} (performance concern)")
        else:
            print(f"    ✓ All tenant_id columns are properly indexed")

        # Check 2: Primary keys exist on all tables
        tables_without_pk = []
        for table_name in self.inspector.get_table_names():
            if table_name == 'alembic_version':
                continue

            pk = self.inspector.get_pk_constraint(table_name)
            if not pk or not pk.get('constrained_columns'):
                tables_without_pk.append(table_name)

        if tables_without_pk:
            for table in tables_without_pk:
                self.results['errors'].append(f"Table {table} has no primary key")
        else:
            print(f"    ✓ All tables have primary keys")

        # Check 3: Foreign keys should have indexes (PostgreSQL best practice)
        unindexed_fks = []
        for table_name in self.inspector.get_table_names():
            if table_name == 'alembic_version':
                continue

            fks = self.inspector.get_foreign_keys(table_name)
            indexes = self.inspector.get_indexes(table_name)

            for fk in fks:
                fk_cols = fk['constrained_columns']
                # Check if FK column is indexed
                is_indexed = any(
                    set(fk_cols).issubset(set(idx['column_names']))
                    for idx in indexes
                )

                if not is_indexed:
                    unindexed_fks.append(f"{table_name}.{', '.join(fk_cols)}")

        if unindexed_fks:
            for fk in unindexed_fks:
                self.results['warnings'].append(f"Foreign key {fk} is not indexed (may impact JOIN performance)")

    def analyze_performance(self):
        """Analyze database performance metrics."""
        print("  Analyzing performance metrics...")

        with self.engine.connect() as conn:
            # Get table sizes and row counts
            for table_name in self.inspector.get_table_names():
                if table_name == 'alembic_version':
                    continue

                try:
                    # Get row count
                    count_query = text(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = conn.execute(count_query).scalar()

                    # Get table size (PostgreSQL specific)
                    size_query = text(f"SELECT pg_total_relation_size('{table_name}')")
                    size_bytes = conn.execute(size_query).scalar()
                    size_mb = size_bytes / (1024 * 1024) if size_bytes else 0

                    if row_count > 0:
                        print(f"    ℹ {table_name:20s}: {row_count:6,d} rows, {size_mb:6.2f} MB")

                    self.results['stats'][f'{table_name}_rows'] = row_count
                    self.results['stats'][f'{table_name}_size_mb'] = round(size_mb, 2)

                except Exception as e:
                    self.results['warnings'].append(f"Could not analyze {table_name}: {str(e)}")

    def print_report(self):
        """Print comprehensive validation report."""
        print("=" * 80)
        print("VALIDATION REPORT")
        print("=" * 80)

        # Summary
        error_count = len(self.results['errors'])
        warning_count = len(self.results['warnings'])
        info_count = len(self.results['info'])

        print(f"\nSummary:")
        print(f"  ✓ Info:     {info_count}")
        print(f"  ⚠ Warnings: {warning_count}")
        print(f"  ✗ Errors:   {error_count}")

        # Errors
        if self.results['errors']:
            print(f"\n{'ERRORS':=^80}")
            for i, error in enumerate(self.results['errors'], 1):
                print(f"  {i}. ✗ {error}")

        # Warnings
        if self.results['warnings']:
            print(f"\n{'WARNINGS':=^80}")
            for i, warning in enumerate(self.results['warnings'], 1):
                print(f"  {i}. ⚠ {warning}")

        # Info
        if self.results['info']:
            print(f"\n{'VALIDATION PASSED':=^80}")
            for info in self.results['info']:
                print(f"  {info}")

        # Statistics
        if self.results['stats']:
            print(f"\n{'DATABASE STATISTICS':=^80}")
            print(f"  Models Registered:    {self.results['stats'].get('registered_models', 0)}")
            print(f"  Database Tables:      {self.results['stats'].get('database_tables', 0)}")
            print(f"  Foreign Keys:         {self.results['stats'].get('foreign_keys', 0)}")

        # Overall Status
        print()
        print("=" * 80)
        if error_count == 0:
            print("✓ DATABASE VALIDATION PASSED")
            print("  All schema validation checks completed successfully.")
        else:
            print("✗ DATABASE VALIDATION FAILED")
            print(f"  Found {error_count} critical issue(s) that need attention.")
            if warning_count > 0:
                print(f"  Also found {warning_count} warning(s) that should be reviewed.")
        print("=" * 80)


def main():
    """Main entry point for database review script."""
    try:
        reviewer = DatabaseReviewer()
        exit_code = reviewer.run_all_checks()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
