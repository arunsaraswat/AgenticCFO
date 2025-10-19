"""Template detection for uploaded files.

Intelligent Implementation: Analyzes data patterns, structure, and content
to automatically detect file type without requiring strict column naming.

This module detects which financial template type an uploaded file represents
(e.g., BankStatement, TrialBalance, AP_OpenItems) by analyzing:
- Column data types (dates, numbers, text)
- Data patterns (balances, transactions, aging buckets)
- Content characteristics (vendors, customers, accounts)
- Statistical distributions
"""
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import re

import pandas as pd
import numpy as np

from app.core.exceptions import TemplateDetectionError


class TemplateDetector:
    """
    Intelligently detects template type from file data patterns.

    Uses heuristic-based analysis rather than strict column name matching.
    """

    @staticmethod
    def detect_from_dataframe(df: pd.DataFrame) -> tuple[Optional[str], float]:
        """
        Detect template type by analyzing data patterns.

        Args:
            df: Pandas DataFrame with data

        Returns:
            Tuple of (template_type, confidence_score)
            Returns (None, 0.0) if no match found

        Example:
            >>> df = pd.read_excel("bank_statement.xlsx")
            >>> template_type, confidence = TemplateDetector.detect_from_dataframe(df)
            >>> print(f"Detected: {template_type} (confidence: {confidence:.2%})")
            Detected: BankStatement (confidence: 0.85)
        """
        if df.empty or len(df.columns) == 0:
            return None, 0.0

        # Analyze the DataFrame structure
        analysis = TemplateDetector._analyze_dataframe(df)

        # Score each template type based on patterns
        scores = {
            "BankStatement": TemplateDetector._score_bank_statement(df, analysis),
            "TrialBalance": TemplateDetector._score_trial_balance(df, analysis),
            "AP_OpenItems": TemplateDetector._score_ap_items(df, analysis),
            "AR_Aging": TemplateDetector._score_ar_aging(df, analysis),
            "POS_Sales": TemplateDetector._score_pos_sales(df, analysis),
        }

        # Find best match
        best_template = max(scores.items(), key=lambda x: x[1])
        template_type, confidence = best_template

        # Require minimum confidence threshold
        if confidence < 0.3:
            return None, 0.0

        return template_type, confidence

    @staticmethod
    def _analyze_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze DataFrame to extract structural patterns.

        Returns:
            Dictionary with analysis results:
            - date_columns: List of column indices that contain dates
            - numeric_columns: List of column indices with numeric data
            - text_columns: List of column indices with text data
            - has_running_balance: Whether there's a column that looks like running balance
            - has_debit_credit: Whether there are paired debit/credit columns
            - has_aging_buckets: Whether there are aging bucket columns (30/60/90 days)
            - num_rows: Number of data rows
            - num_columns: Number of columns
        """
        analysis = {
            "date_columns": [],
            "numeric_columns": [],
            "text_columns": [],
            "has_running_balance": False,
            "has_debit_credit": False,
            "has_aging_buckets": False,
            "has_account_numbers": False,
            "has_sequential_dates": False,
            "num_rows": len(df),
            "num_columns": len(df.columns),
        }

        # Analyze each column
        for idx, col in enumerate(df.columns):
            col_data = df[col].dropna()

            if len(col_data) == 0:
                continue

            # Check if column contains dates
            if TemplateDetector._is_date_column(col_data):
                analysis["date_columns"].append(idx)

                # Check if dates are sequential (typical of bank statements)
                if TemplateDetector._has_sequential_dates(col_data):
                    analysis["has_sequential_dates"] = True

            # Check if column is numeric
            elif TemplateDetector._is_numeric_column(col_data):
                analysis["numeric_columns"].append(idx)

                # Check for running balance pattern
                if TemplateDetector._looks_like_running_balance(col_data):
                    analysis["has_running_balance"] = True

            # Otherwise it's text
            else:
                analysis["text_columns"].append(idx)

                # Check for account numbers (typical of trial balance)
                if TemplateDetector._looks_like_account_numbers(col_data):
                    analysis["has_account_numbers"] = True

        # Check for debit/credit pairs
        if len(analysis["numeric_columns"]) >= 2:
            analysis["has_debit_credit"] = TemplateDetector._has_debit_credit_pattern(df, analysis["numeric_columns"])

        # Check for aging buckets (30/60/90/120 day columns)
        if len(analysis["numeric_columns"]) >= 3:
            analysis["has_aging_buckets"] = TemplateDetector._has_aging_bucket_pattern(df, analysis["numeric_columns"])

        return analysis

    @staticmethod
    def _score_bank_statement(df: pd.DataFrame, analysis: Dict[str, Any]) -> float:
        """
        Score likelihood that this is a bank statement.

        Bank statement characteristics:
        - Has date column (sequential dates)
        - Has transaction description (text column)
        - Has amount column(s) - often debit/credit or single amount
        - Often has running balance column
        - Usually 3-6 columns
        - Transactions are chronological
        """
        score = 0.0

        # Must have at least one date column
        if len(analysis["date_columns"]) == 0:
            return 0.0

        # Date column is present (+30%)
        score += 0.3

        # Sequential dates (typical of bank statements) (+20%)
        if analysis["has_sequential_dates"]:
            score += 0.2

        # Has running balance (+20%)
        if analysis["has_running_balance"]:
            score += 0.2

        # Has text column for descriptions (+10%)
        if len(analysis["text_columns"]) >= 1:
            score += 0.1

        # Has 1-3 numeric columns (amount, balance, etc.) (+10%)
        if 1 <= len(analysis["numeric_columns"]) <= 3:
            score += 0.1

        # Reasonable column count for bank statement (3-6 columns) (+10%)
        if 3 <= analysis["num_columns"] <= 6:
            score += 0.1

        return min(score, 1.0)

    @staticmethod
    def _score_trial_balance(df: pd.DataFrame, analysis: Dict[str, Any]) -> float:
        """
        Score likelihood that this is a trial balance.

        Trial balance characteristics:
        - Has account numbers or GL codes
        - Has debit and credit columns (two numeric columns)
        - May have account descriptions
        - Usually no date column (or single period date)
        - Debits and credits should balance
        """
        score = 0.0

        # Should NOT have sequential dates (trial balance is point-in-time)
        if analysis["has_sequential_dates"]:
            return 0.0

        # Has account numbers (+30%)
        if analysis["has_account_numbers"]:
            score += 0.3

        # Has debit/credit pattern (+40%)
        if analysis["has_debit_credit"]:
            score += 0.4

        # Has text columns (account descriptions) (+15%)
        if len(analysis["text_columns"]) >= 1:
            score += 0.15

        # Has appropriate column count (typically 3-5) (+15%)
        if 3 <= analysis["num_columns"] <= 5:
            score += 0.15

        return min(score, 1.0)

    @staticmethod
    def _score_ap_items(df: pd.DataFrame, analysis: Dict[str, Any]) -> float:
        """
        Score likelihood that this is AP open items.

        AP characteristics:
        - Has vendor names (text column)
        - Has invoice dates or due dates
        - Has amounts
        - May have aging buckets
        - May have invoice numbers
        """
        score = 0.0

        # Should have date column(s) (+20%)
        if len(analysis["date_columns"]) >= 1:
            score += 0.2

        # Has text columns (vendor names, invoice numbers) (+25%)
        if len(analysis["text_columns"]) >= 1:
            score += 0.25

        # Has aging buckets (+30%)
        if analysis["has_aging_buckets"]:
            score += 0.3

        # Has multiple numeric columns (+15%)
        if len(analysis["numeric_columns"]) >= 2:
            score += 0.15

        # Appropriate column count (4-8 for AP aging) (+10%)
        if 4 <= analysis["num_columns"] <= 8:
            score += 0.1

        return min(score, 1.0)

    @staticmethod
    def _score_ar_aging(df: pd.DataFrame, analysis: Dict[str, Any]) -> float:
        """
        Score likelihood that this is AR aging.

        AR characteristics:
        - Has customer names (text column)
        - Has invoice dates or due dates
        - Has amounts
        - May have aging buckets (current, 30, 60, 90, 120+)
        - Similar to AP but with customer focus
        """
        score = 0.0

        # Should have date column(s) (+20%)
        if len(analysis["date_columns"]) >= 1:
            score += 0.2

        # Has text columns (customer names, invoice numbers) (+25%)
        if len(analysis["text_columns"]) >= 1:
            score += 0.25

        # Has aging buckets (+35%)
        if analysis["has_aging_buckets"]:
            score += 0.35

        # Has multiple numeric columns (+10%)
        if len(analysis["numeric_columns"]) >= 2:
            score += 0.1

        # Appropriate column count (+10%)
        if 4 <= analysis["num_columns"] <= 8:
            score += 0.1

        return min(score, 1.0)

    @staticmethod
    def _score_pos_sales(df: pd.DataFrame, analysis: Dict[str, Any]) -> float:
        """
        Score likelihood that this is POS sales data.

        POS characteristics:
        - Has dates (transaction dates)
        - Has product/SKU information (text)
        - Has quantities (numeric, typically integers)
        - Has amounts/prices
        - May have store/location
        - High transaction volume
        """
        score = 0.0

        # Must have date column (+20%)
        if len(analysis["date_columns"]) == 0:
            return 0.0
        score += 0.2

        # Has text columns (product, SKU, store) (+20%)
        if len(analysis["text_columns"]) >= 2:
            score += 0.2

        # Has multiple numeric columns (qty, price, amount) (+20%)
        if len(analysis["numeric_columns"]) >= 2:
            score += 0.2

        # High row count (POS usually has many transactions) (+20%)
        if analysis["num_rows"] > 100:
            score += 0.2

        # Appropriate column count (+20%)
        if 4 <= analysis["num_columns"] <= 10:
            score += 0.2

        return min(score, 1.0)

    # Helper methods for pattern detection

    @staticmethod
    def _is_date_column(series: pd.Series) -> bool:
        """Check if column contains dates."""
        # Try to parse as datetime
        try:
            # Sample first few non-null values
            sample = series.dropna().head(10)
            if len(sample) == 0:
                return False

            # Try pandas datetime conversion
            parsed = pd.to_datetime(sample, errors='coerce')
            valid_dates = parsed.notna().sum()

            # If >70% are valid dates, consider it a date column
            return (valid_dates / len(sample)) > 0.7

        except:
            return False

    @staticmethod
    def _is_numeric_column(series: pd.Series) -> bool:
        """Check if column is numeric."""
        # Check if already numeric dtype
        if pd.api.types.is_numeric_dtype(series):
            return True

        # Try to convert to numeric
        try:
            sample = series.dropna().head(10)
            if len(sample) == 0:
                return False

            # Remove common currency symbols and commas
            cleaned = sample.astype(str).str.replace(r'[$,]', '', regex=True)
            numeric = pd.to_numeric(cleaned, errors='coerce')
            valid_numbers = numeric.notna().sum()

            # If >70% are valid numbers, consider it numeric
            return (valid_numbers / len(sample)) > 0.7

        except:
            return False

    @staticmethod
    def _has_sequential_dates(series: pd.Series) -> bool:
        """Check if dates are mostly sequential (typical of bank statements)."""
        try:
            dates = pd.to_datetime(series.dropna(), errors='coerce').dropna()
            if len(dates) < 2:
                return False

            # Check if dates are sorted
            sorted_dates = dates.sort_values()
            date_diffs = sorted_dates.diff().dt.days.dropna()

            # Most differences should be small (1-7 days for daily transactions)
            if len(date_diffs) == 0:
                return False

            return date_diffs.median() <= 7

        except:
            return False

    @staticmethod
    def _looks_like_running_balance(series: pd.Series) -> bool:
        """Check if numeric column looks like a running balance."""
        try:
            numeric = pd.to_numeric(series, errors='coerce').dropna()
            if len(numeric) < 3:
                return False

            # Running balance typically:
            # 1. Is always positive (or always negative)
            # 2. Changes gradually (not wildly volatile)
            # 3. May have a trend

            all_positive = (numeric > 0).all()
            all_negative = (numeric < 0).all()

            if not (all_positive or all_negative):
                return False

            # Check for gradual changes (coefficient of variation)
            cv = numeric.std() / numeric.mean() if numeric.mean() != 0 else float('inf')

            # Running balance typically has CV < 2 (not too volatile)
            return cv < 2.0

        except:
            return False

    @staticmethod
    def _looks_like_account_numbers(series: pd.Series) -> bool:
        """Check if text column contains account numbers."""
        try:
            sample = series.dropna().astype(str).head(20)
            if len(sample) == 0:
                return False

            # Account numbers typically:
            # 1. Contain digits
            # 2. Have consistent length
            # 3. May have consistent format (e.g., XXXX-XXXX)

            has_digits = sample.str.contains(r'\d', regex=True).sum()

            # Check if most values have digits
            if (has_digits / len(sample)) < 0.7:
                return False

            # Check for consistent length
            lengths = sample.str.len()
            length_std = lengths.std()

            # Account numbers usually have consistent length (std < 3)
            return length_std < 3.0

        except:
            return False

    @staticmethod
    def _has_debit_credit_pattern(df: pd.DataFrame, numeric_cols: List[int]) -> bool:
        """Check if there are paired debit/credit columns."""
        if len(numeric_cols) < 2:
            return False

        try:
            # Check pairs of numeric columns
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    col1 = df.iloc[:, numeric_cols[i]]
                    col2 = df.iloc[:, numeric_cols[j]]

                    # Convert to numeric
                    num1 = pd.to_numeric(col1, errors='coerce')
                    num2 = pd.to_numeric(col2, errors='coerce')

                    # Check if columns are mutually exclusive (typical of DR/CR)
                    # One has value, other is null/zero
                    mask1 = (num1.notna() & (num1 != 0) & ((num2.isna()) | (num2 == 0)))
                    mask2 = (num2.notna() & (num2 != 0) & ((num1.isna()) | (num1 == 0)))

                    mutual_exclusive_pct = (mask1.sum() + mask2.sum()) / len(df)

                    # If >60% are mutually exclusive, likely debit/credit
                    if mutual_exclusive_pct > 0.6:
                        return True

            return False

        except:
            return False

    @staticmethod
    def _has_aging_bucket_pattern(df: pd.DataFrame, numeric_cols: List[int]) -> bool:
        """Check if there are aging bucket columns (current, 30, 60, 90, 120+)."""
        if len(numeric_cols) < 3:
            return False

        try:
            # Look for column names that suggest aging buckets
            col_names = [str(df.columns[i]).lower() for i in numeric_cols]

            aging_keywords = ['current', '30', '60', '90', '120', 'days', 'aging']
            matches = sum(1 for name in col_names if any(kw in name for kw in aging_keywords))

            # If 3+ numeric columns have aging keywords, likely aging report
            return matches >= 3

        except:
            return False

    @staticmethod
    def get_supported_templates() -> List[str]:
        """
        Get list of supported template types.

        Returns:
            List of template type names
        """
        return ["BankStatement", "TrialBalance", "AP_OpenItems", "AR_Aging", "POS_Sales"]

    @staticmethod
    def get_template_description(template_type: str) -> Optional[str]:
        """
        Get human-readable description of template type.

        Args:
            template_type: Template type name

        Returns:
            Description string or None if not found
        """
        descriptions = {
            "BankStatement": "Bank statement with transactions, dates, and running balance",
            "TrialBalance": "General ledger trial balance with accounts, debits, and credits",
            "AP_OpenItems": "Accounts payable open items with vendors and due dates",
            "AR_Aging": "Accounts receivable aging report with customers and aging buckets",
            "POS_Sales": "Point-of-sale transactions with products, quantities, and amounts",
        }
        return descriptions.get(template_type)
