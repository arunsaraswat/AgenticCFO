"""Template detection for uploaded files.

MVP Implementation: Rule-based keyword matching
Future: ML-based classification with confidence scores

This module detects which financial template type an uploaded file represents
(e.g., BankStatement, TrialBalance, AP_OpenItems) by analyzing column headers.
"""
from typing import Optional

import pandas as pd

from app.core.exceptions import TemplateDetectionError


class TemplateDetector:
    """
    Detects template type from file column headers.

    MVP: Uses keyword matching against known patterns
    Phase 2: Will use ML classifier trained on historical uploads
    """

    # Template signatures: keywords that strongly indicate template type
    # NOTE: In Phase 2, this will be replaced with ChromaDB semantic search
    # and ML-based classification for better accuracy
    TEMPLATE_SIGNATURES = {
        "BankStatement": {
            "required_keywords": ["date", "description", "amount"],
            "optional_keywords": ["balance", "debit", "credit", "withdrawal", "deposit"],
            "min_match_score": 2,  # Need at least 2 keyword matches
        },
        "TrialBalance": {
            "required_keywords": ["account", "debit", "credit"],
            "optional_keywords": ["balance", "description", "account number", "gl"],
            "min_match_score": 3,
        },
        "AP_OpenItems": {
            "required_keywords": ["vendor", "invoice", "amount"],
            "optional_keywords": ["due date", "invoice date", "payment terms", "aging"],
            "min_match_score": 3,
        },
        "AR_Aging": {
            "required_keywords": ["customer", "invoice", "amount"],
            "optional_keywords": ["due date", "invoice date", "aging", "current", "30 days"],
            "min_match_score": 3,
        },
        "POS_Sales": {
            "required_keywords": ["date", "product", "quantity", "amount"],
            "optional_keywords": ["store", "sku", "price", "total"],
            "min_match_score": 3,
        },
    }

    @staticmethod
    def normalize_column_name(col: str) -> str:
        """
        Normalize column name for matching.

        Args:
            col: Raw column name

        Returns:
            Normalized lowercase string with stripped whitespace
        """
        return str(col).lower().strip()

    @staticmethod
    def detect_from_dataframe(df: pd.DataFrame) -> tuple[Optional[str], float]:
        """
        Detect template type from DataFrame columns.

        Args:
            df: Pandas DataFrame with headers

        Returns:
            Tuple of (template_type, confidence_score)
            Returns (None, 0.0) if no match found

        Example:
            >>> df = pd.read_excel("bank_statement.xlsx")
            >>> template_type, confidence = TemplateDetector.detect_from_dataframe(df)
            >>> print(f"Detected: {template_type} (confidence: {confidence:.2%})")
            Detected: BankStatement (confidence: 0.85)
        """
        # Get normalized column names
        columns = [TemplateDetector.normalize_column_name(col) for col in df.columns]

        best_match = None
        best_score = 0.0

        # Score each template type
        for template_type, signature in TemplateDetector.TEMPLATE_SIGNATURES.items():
            score = TemplateDetector._calculate_match_score(
                columns, signature["required_keywords"], signature["optional_keywords"]
            )

            # Check if minimum threshold met
            if score >= signature["min_match_score"]:
                # Calculate confidence as percentage of total possible matches
                max_possible = len(signature["required_keywords"]) + len(
                    signature["optional_keywords"]
                )
                confidence = score / max_possible

                if confidence > best_score:
                    best_match = template_type
                    best_score = confidence

        return best_match, best_score

    @staticmethod
    def _calculate_match_score(
        columns: list[str], required_keywords: list[str], optional_keywords: list[str]
    ) -> float:
        """
        Calculate match score for a template signature.

        Required keywords must ALL be present (with fuzzy matching).
        Optional keywords contribute to score but aren't required.

        Args:
            columns: Normalized column names from file
            required_keywords: Keywords that must be present
            optional_keywords: Keywords that boost score if present

        Returns:
            Match score (0.0 if required keywords not found)
        """
        # Check required keywords with fuzzy matching
        required_matches = 0
        for keyword in required_keywords:
            if TemplateDetector._fuzzy_match_keyword(keyword, columns):
                required_matches += 1

        # If not all required keywords found, return 0
        if required_matches < len(required_keywords):
            return 0.0

        # Count optional keyword matches
        optional_matches = 0
        for keyword in optional_keywords:
            if TemplateDetector._fuzzy_match_keyword(keyword, columns):
                optional_matches += 1

        # Total score: required + optional matches
        return required_matches + optional_matches

    @staticmethod
    def _fuzzy_match_keyword(keyword: str, columns: list[str]) -> bool:
        """
        Check if keyword appears in any column name (fuzzy match).

        Uses substring matching: "date" matches "transaction_date", "post_date", etc.

        NOTE: In Phase 2, this will be replaced with:
        - ChromaDB semantic similarity search
        - Learned embeddings from historical mappings
        - 90%+ reuse rate after first mapping cycle

        Args:
            keyword: Keyword to search for (normalized)
            columns: List of normalized column names

        Returns:
            True if keyword found in any column
        """
        keyword = keyword.lower().strip()

        for col in columns:
            # Check if keyword is substring of column name
            if keyword in col:
                return True

            # Check if column name is substring of keyword (handles "desc" matching "description")
            if len(col) >= 3 and col in keyword:
                return True

        return False

    @staticmethod
    def get_supported_templates() -> list[str]:
        """
        Get list of supported template types.

        Returns:
            List of template type names
        """
        return list(TemplateDetector.TEMPLATE_SIGNATURES.keys())

    @staticmethod
    def get_template_signature(template_type: str) -> Optional[dict]:
        """
        Get signature for a specific template type.

        Args:
            template_type: Template type name

        Returns:
            Template signature dict or None if not found
        """
        return TemplateDetector.TEMPLATE_SIGNATURES.get(template_type)
