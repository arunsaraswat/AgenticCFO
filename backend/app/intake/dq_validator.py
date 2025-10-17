"""Data Quality validation for uploaded datasets.

MVP Implementation: Rule-based validators (required columns, date formats, numeric validation, duplicates)
Future: ML-based anomaly detection, statistical outlier detection, cross-file reconciliation

This module validates data quality after parsing and mapping to catch issues before agent processing.
"""
from datetime import datetime
from typing import Any, Optional

import pandas as pd


class DQValidationResult:
    """
    Data quality validation result.

    Attributes:
        status: Validation status (passed, warning, failed)
        checks: Dictionary of check results
        error_count: Number of failed checks
        warning_count: Number of warning checks
    """

    def __init__(self):
        self.status: str = "passed"
        self.checks: dict[str, dict[str, Any]] = {}
        self.error_count: int = 0
        self.warning_count: int = 0

    def add_check(
        self,
        check_name: str,
        status: str,
        message: str,
        details: Optional[dict] = None,
    ):
        """
        Add a validation check result.

        Args:
            check_name: Name of the check
            status: Check status (passed, warning, failed)
            message: Human-readable message
            details: Additional details (optional)
        """
        self.checks[check_name] = {
            "status": status,
            "message": message,
            "details": details or {},
        }

        if status == "failed":
            self.error_count += 1
            self.status = "failed"
        elif status == "warning" and self.status != "failed":
            self.warning_count += 1
            if self.status == "passed":
                self.status = "warning"

    def to_dict(self) -> dict:
        """
        Convert result to dictionary.

        Returns:
            Dictionary representation of validation result
        """
        return {
            "status": self.status,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "checks": self.checks,
        }


class DQValidator:
    """
    Data quality validator for uploaded datasets.

    MVP: Rule-based validation checks
    Phase 2: Will add ML-based anomaly detection, statistical outlier detection
    """

    # Maximum percentage of null values allowed per column
    MAX_NULL_PERCENTAGE = 0.5  # 50%

    # Date format patterns to try
    DATE_FORMATS = [
        "%Y-%m-%d",  # 2025-01-15
        "%m/%d/%Y",  # 01/15/2025
        "%d/%m/%Y",  # 15/01/2025
        "%Y/%m/%d",  # 2025/01/15
        "%m-%d-%Y",  # 01-15-2025
        "%d-%m-%Y",  # 15-01-2025
        "%b %d, %Y",  # Jan 15, 2025
        "%B %d, %Y",  # January 15, 2025
        "%d-%b-%Y",  # 15-Jan-2025
    ]

    @staticmethod
    def validate_dataset(
        df: pd.DataFrame,
        template_type: str,
        column_mappings: dict[str, Optional[str]],
    ) -> DQValidationResult:
        """
        Validate dataset quality.

        Runs multiple validation checks:
        1. Required columns present
        2. Date format validation
        3. Numeric column validation
        4. Duplicate detection
        5. Null value analysis

        Args:
            df: Pandas DataFrame with data
            template_type: Template type (e.g., "BankStatement")
            column_mappings: Mapping of standard columns to source columns

        Returns:
            DQValidationResult with all check results

        Note:
            In Phase 2, will add:
            - Cross-file reconciliation (e.g., bank statement balance vs GL)
            - Statistical outlier detection using Z-scores
            - ML-based anomaly detection
            - Time series validation (gaps, inconsistencies)
        """
        result = DQValidationResult()

        # Check 1: Required columns
        DQValidator._check_required_columns(df, template_type, column_mappings, result)

        # Check 2: Date format validation
        DQValidator._check_date_formats(df, column_mappings, result)

        # Check 3: Numeric column validation
        DQValidator._check_numeric_columns(df, column_mappings, result)

        # Check 4: Duplicate detection
        DQValidator._check_duplicates(df, column_mappings, result)

        # Check 5: Null value analysis
        DQValidator._check_null_values(df, column_mappings, result)

        # Check 6: Row count validation
        DQValidator._check_row_count(df, result)

        return result

    @staticmethod
    def _check_required_columns(
        df: pd.DataFrame,
        template_type: str,
        column_mappings: dict[str, Optional[str]],
        result: DQValidationResult,
    ):
        """
        Check that all required columns are present and mapped.

        Args:
            df: DataFrame
            template_type: Template type
            column_mappings: Column mappings
            result: Validation result to update
        """
        # Get required columns for template type
        from app.intake.column_mapper import ColumnMapper

        required_columns = ColumnMapper.get_required_columns(template_type)
        missing_columns = []

        for col in required_columns:
            if col not in column_mappings or column_mappings[col] is None:
                missing_columns.append(col)

        if missing_columns:
            result.add_check(
                check_name="required_columns",
                status="failed",
                message=f"Missing required columns: {', '.join(missing_columns)}",
                details={"missing_columns": missing_columns},
            )
        else:
            result.add_check(
                check_name="required_columns",
                status="passed",
                message="All required columns present",
                details={"required_columns": required_columns},
            )

    @staticmethod
    def _check_date_formats(
        df: pd.DataFrame,
        column_mappings: dict[str, Optional[str]],
        result: DQValidationResult,
    ):
        """
        Validate date columns can be parsed.

        Args:
            df: DataFrame
            column_mappings: Column mappings
            result: Validation result to update
        """
        # Find date columns (columns with "date" in standard name)
        date_columns = [
            (std_col, src_col)
            for std_col, src_col in column_mappings.items()
            if "date" in std_col.lower() and src_col is not None
        ]

        if not date_columns:
            return

        date_check_details = {}

        for std_col, src_col in date_columns:
            if src_col not in df.columns:
                continue

            # Try to parse dates
            parsed_count = 0
            total_count = df[src_col].notna().sum()

            if total_count == 0:
                date_check_details[std_col] = {
                    "source_column": src_col,
                    "status": "warning",
                    "message": "Column is empty",
                }
                continue

            # Try different date formats
            for date_format in DQValidator.DATE_FORMATS:
                try:
                    parsed = pd.to_datetime(
                        df[src_col], format=date_format, errors="coerce"
                    )
                    parsed_count = parsed.notna().sum()

                    if parsed_count / total_count >= 0.8:  # 80% success rate
                        date_check_details[std_col] = {
                            "source_column": src_col,
                            "status": "passed",
                            "format": date_format,
                            "parsed_percentage": round(parsed_count / total_count * 100, 2),
                        }
                        break
                except Exception:
                    continue

            # If no format worked well
            if std_col not in date_check_details:
                date_check_details[std_col] = {
                    "source_column": src_col,
                    "status": "failed",
                    "message": "Could not parse dates with standard formats",
                }

        # Determine overall status
        failed_dates = [
            col for col, details in date_check_details.items() if details["status"] == "failed"
        ]

        if failed_dates:
            result.add_check(
                check_name="date_formats",
                status="failed",
                message=f"Date parsing failed for: {', '.join(failed_dates)}",
                details=date_check_details,
            )
        else:
            result.add_check(
                check_name="date_formats",
                status="passed",
                message="All date columns validated",
                details=date_check_details,
            )

    @staticmethod
    def _check_numeric_columns(
        df: pd.DataFrame,
        column_mappings: dict[str, Optional[str]],
        result: DQValidationResult,
    ):
        """
        Validate numeric columns (amounts, quantities, etc.).

        Args:
            df: DataFrame
            column_mappings: Column mappings
            result: Validation result to update
        """
        # Find numeric columns
        numeric_keywords = ["amount", "quantity", "qty", "price", "balance", "total"]
        numeric_columns = [
            (std_col, src_col)
            for std_col, src_col in column_mappings.items()
            if any(keyword in std_col.lower() for keyword in numeric_keywords)
            and src_col is not None
        ]

        if not numeric_columns:
            return

        numeric_check_details = {}

        for std_col, src_col in numeric_columns:
            if src_col not in df.columns:
                continue

            # Try to convert to numeric
            try:
                numeric_series = pd.to_numeric(df[src_col], errors="coerce")
                valid_count = numeric_series.notna().sum()
                total_count = df[src_col].notna().sum()

                if total_count == 0:
                    numeric_check_details[std_col] = {
                        "source_column": src_col,
                        "status": "warning",
                        "message": "Column is empty",
                    }
                    continue

                valid_percentage = valid_count / total_count * 100

                if valid_percentage >= 80:  # 80% valid numbers
                    numeric_check_details[std_col] = {
                        "source_column": src_col,
                        "status": "passed",
                        "valid_percentage": round(valid_percentage, 2),
                        "min": float(numeric_series.min()),
                        "max": float(numeric_series.max()),
                        "mean": float(numeric_series.mean()),
                    }
                else:
                    numeric_check_details[std_col] = {
                        "source_column": src_col,
                        "status": "failed",
                        "valid_percentage": round(valid_percentage, 2),
                        "message": f"Only {valid_percentage:.1f}% of values are valid numbers",
                    }

            except Exception as e:
                numeric_check_details[std_col] = {
                    "source_column": src_col,
                    "status": "failed",
                    "message": f"Error parsing numeric column: {str(e)}",
                }

        # Determine overall status
        failed_numeric = [
            col for col, details in numeric_check_details.items() if details["status"] == "failed"
        ]

        if failed_numeric:
            result.add_check(
                check_name="numeric_columns",
                status="warning",
                message=f"Numeric validation issues in: {', '.join(failed_numeric)}",
                details=numeric_check_details,
            )
        else:
            result.add_check(
                check_name="numeric_columns",
                status="passed",
                message="All numeric columns validated",
                details=numeric_check_details,
            )

    @staticmethod
    def _check_duplicates(
        df: pd.DataFrame,
        column_mappings: dict[str, Optional[str]],
        result: DQValidationResult,
    ):
        """
        Check for duplicate rows.

        Args:
            df: DataFrame
            column_mappings: Column mappings
            result: Validation result to update
        """
        # Get key columns for duplicate detection (varies by template)
        key_columns = []
        for std_col, src_col in column_mappings.items():
            if src_col and std_col in [
                "transaction_date",
                "invoice_number",
                "reference_number",
                "product_code",
                "account_code",
            ]:
                if src_col in df.columns:
                    key_columns.append(src_col)

        if not key_columns:
            # Fall back to checking exact duplicate rows
            duplicate_count = df.duplicated().sum()
            total_rows = len(df)

            if duplicate_count > 0:
                result.add_check(
                    check_name="duplicates",
                    status="warning",
                    message=f"Found {duplicate_count} exact duplicate rows",
                    details={
                        "duplicate_count": int(duplicate_count),
                        "duplicate_percentage": round(duplicate_count / total_rows * 100, 2),
                    },
                )
            else:
                result.add_check(
                    check_name="duplicates",
                    status="passed",
                    message="No duplicate rows found",
                    details={"duplicate_count": 0},
                )
        else:
            # Check duplicates based on key columns
            duplicate_count = df.duplicated(subset=key_columns).sum()
            total_rows = len(df)

            if duplicate_count > 0:
                result.add_check(
                    check_name="duplicates",
                    status="warning",
                    message=f"Found {duplicate_count} duplicate rows based on key columns",
                    details={
                        "duplicate_count": int(duplicate_count),
                        "duplicate_percentage": round(duplicate_count / total_rows * 100, 2),
                        "key_columns": key_columns,
                    },
                )
            else:
                result.add_check(
                    check_name="duplicates",
                    status="passed",
                    message="No duplicates found in key columns",
                    details={"duplicate_count": 0, "key_columns": key_columns},
                )

    @staticmethod
    def _check_null_values(
        df: pd.DataFrame,
        column_mappings: dict[str, Optional[str]],
        result: DQValidationResult,
    ):
        """
        Analyze null values in mapped columns.

        Args:
            df: DataFrame
            column_mappings: Column mappings
            result: Validation result to update
        """
        null_analysis = {}
        high_null_columns = []

        for std_col, src_col in column_mappings.items():
            if src_col and src_col in df.columns:
                null_count = df[src_col].isna().sum()
                total_count = len(df)
                null_percentage = null_count / total_count

                null_analysis[std_col] = {
                    "source_column": src_col,
                    "null_count": int(null_count),
                    "null_percentage": round(null_percentage * 100, 2),
                }

                if null_percentage > DQValidator.MAX_NULL_PERCENTAGE:
                    high_null_columns.append(std_col)

        if high_null_columns:
            result.add_check(
                check_name="null_values",
                status="warning",
                message=f"High null percentage in: {', '.join(high_null_columns)}",
                details=null_analysis,
            )
        else:
            result.add_check(
                check_name="null_values",
                status="passed",
                message="Null values within acceptable limits",
                details=null_analysis,
            )

    @staticmethod
    def _check_row_count(df: pd.DataFrame, result: DQValidationResult):
        """
        Validate minimum row count.

        Args:
            df: DataFrame
            result: Validation result to update
        """
        row_count = len(df)
        min_rows = 1  # Minimum 1 row required

        if row_count < min_rows:
            result.add_check(
                check_name="row_count",
                status="failed",
                message=f"Insufficient data: only {row_count} rows",
                details={"row_count": row_count, "min_required": min_rows},
            )
        elif row_count < 10:
            result.add_check(
                check_name="row_count",
                status="warning",
                message=f"Low row count: {row_count} rows (recommend 10+)",
                details={"row_count": row_count},
            )
        else:
            result.add_check(
                check_name="row_count",
                status="passed",
                message=f"Dataset has {row_count} rows",
                details={"row_count": row_count},
            )
