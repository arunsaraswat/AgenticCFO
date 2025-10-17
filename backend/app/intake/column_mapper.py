"""Column mapping service for standardizing file columns to template schemas.

MVP Implementation: Rule-based pattern matching with fuzzy logic
Future: ChromaDB semantic search with learned embeddings

This module maps raw column names from uploaded files to standardized template columns.
For example: "Trans Date" → "transaction_date", "Amount Dr" → "debit_amount"
"""
from typing import Optional

from difflib import SequenceMatcher

from app.core.exceptions import ColumnMappingError


class ColumnMapper:
    """
    Maps source columns to standardized template columns.

    MVP: Uses rule-based pattern matching with fuzzy string matching
    Phase 2: Will use ChromaDB for semantic similarity search
           - Stores all historical mappings as embeddings
           - Learns from user corrections
           - Achieves 90%+ reuse rate after first cycle
    """

    # Standard column patterns for each template type
    # NOTE: In Phase 2, these will be stored in ChromaDB as embeddings
    # New variations will be learned from each upload and user feedback
    TEMPLATE_SCHEMAS = {
        "BankStatement": {
            "transaction_date": [
                "date",
                "trans date",
                "transaction date",
                "posting date",
                "value date",
                "post date",
                "dt",
            ],
            "description": [
                "description",
                "desc",
                "narrative",
                "details",
                "transaction details",
                "memo",
                "reference",
            ],
            "debit_amount": [
                "debit",
                "withdrawal",
                "withdrawals",
                "outgoing",
                "payments",
                "dr",
                "amount dr",
                "debit amount",
            ],
            "credit_amount": [
                "credit",
                "deposit",
                "deposits",
                "incoming",
                "receipts",
                "cr",
                "amount cr",
                "credit amount",
            ],
            "balance": [
                "balance",
                "running balance",
                "ending balance",
                "closing balance",
                "bal",
                "available balance",
            ],
            "reference_number": [
                "reference",
                "ref",
                "check number",
                "cheque number",
                "transaction id",
                "trans id",
            ],
        },
        "TrialBalance": {
            "account_code": [
                "account",
                "account number",
                "account no",
                "gl account",
                "gl code",
                "acct",
            ],
            "account_name": [
                "account name",
                "account description",
                "description",
                "name",
                "gl name",
            ],
            "debit_amount": ["debit", "dr", "debit balance", "debit amount"],
            "credit_amount": ["credit", "cr", "credit balance", "credit amount"],
            "balance": ["balance", "ending balance", "net balance"],
        },
        "AP_OpenItems": {
            "vendor_name": ["vendor", "vendor name", "supplier", "supplier name", "payee"],
            "vendor_code": [
                "vendor code",
                "vendor id",
                "vendor number",
                "supplier code",
                "supplier id",
            ],
            "invoice_number": [
                "invoice",
                "invoice number",
                "invoice no",
                "inv no",
                "document number",
            ],
            "invoice_date": ["invoice date", "inv date", "document date", "date"],
            "due_date": ["due date", "payment due", "maturity date"],
            "amount": [
                "amount",
                "invoice amount",
                "total",
                "open amount",
                "outstanding",
            ],
            "currency": ["currency", "curr", "ccy"],
        },
        "AR_Aging": {
            "customer_name": ["customer", "customer name", "client", "client name"],
            "customer_code": [
                "customer code",
                "customer id",
                "customer number",
                "client code",
            ],
            "invoice_number": ["invoice", "invoice number", "invoice no", "inv no"],
            "invoice_date": ["invoice date", "inv date", "date"],
            "due_date": ["due date", "payment due"],
            "amount": ["amount", "invoice amount", "total", "outstanding"],
            "current": ["current", "0-30", "not due"],
            "days_30": ["30 days", "31-60", "1-30"],
            "days_60": ["60 days", "61-90", "31-60"],
            "days_90_plus": ["90+ days", "over 90", ">90", "90+"],
        },
        "POS_Sales": {
            "transaction_date": ["date", "sale date", "trans date", "transaction date"],
            "store_code": ["store", "store code", "store number", "location", "store id"],
            "product_code": ["product", "product code", "sku", "item code", "item number"],
            "product_name": ["product name", "item name", "description", "item desc"],
            "quantity": ["quantity", "qty", "units", "units sold"],
            "unit_price": ["price", "unit price", "selling price", "retail price"],
            "total_amount": ["amount", "total", "total amount", "sales amount", "revenue"],
        },
    }

    # Minimum similarity threshold for fuzzy matching (0.0 to 1.0)
    SIMILARITY_THRESHOLD = 0.6

    @staticmethod
    def normalize_column_name(col: str) -> str:
        """
        Normalize column name for matching.

        Args:
            col: Raw column name

        Returns:
            Normalized lowercase string
        """
        return str(col).lower().strip().replace("_", " ").replace("-", " ")

    @staticmethod
    def map_columns(
        source_columns: list[str], template_type: str
    ) -> dict[str, Optional[str]]:
        """
        Map source columns to template schema.

        Args:
            source_columns: List of raw column names from file
            template_type: Template type (e.g., "BankStatement")

        Returns:
            Dictionary mapping standard column names to source column names
            Example: {"transaction_date": "Trans Date", "debit_amount": "Withdrawal"}

        Note:
            In Phase 2, this will use ChromaDB to:
            1. Query similar column names from historical mappings
            2. Return top-k matches with confidence scores
            3. Learn from user corrections (feedback loop)
            4. Achieve 90%+ mapping reuse after first cycle
        """
        if template_type not in ColumnMapper.TEMPLATE_SCHEMAS:
            return {}

        schema = ColumnMapper.TEMPLATE_SCHEMAS[template_type]
        mappings = {}

        # Track which source columns have been mapped (avoid double-mapping)
        mapped_sources = set()

        # For each standard column, find best matching source column
        for standard_col, patterns in schema.items():
            best_match = None
            best_score = 0.0

            for source_col in source_columns:
                # Skip if already mapped
                if source_col in mapped_sources:
                    continue

                # Calculate match score
                score = ColumnMapper._calculate_column_similarity(
                    source_col, patterns
                )

                if score > best_score and score >= ColumnMapper.SIMILARITY_THRESHOLD:
                    best_score = score
                    best_match = source_col

            if best_match:
                mappings[standard_col] = best_match
                mapped_sources.add(best_match)
            else:
                mappings[standard_col] = None

        return mappings

    @staticmethod
    def _calculate_column_similarity(source_col: str, patterns: list[str]) -> float:
        """
        Calculate similarity score between source column and pattern list.

        Uses both exact substring matching and fuzzy string similarity.

        Args:
            source_col: Source column name
            patterns: List of known pattern variations

        Returns:
            Similarity score (0.0 to 1.0)
        """
        normalized_source = ColumnMapper.normalize_column_name(source_col)
        best_score = 0.0

        for pattern in patterns:
            normalized_pattern = ColumnMapper.normalize_column_name(pattern)

            # Exact match
            if normalized_source == normalized_pattern:
                return 1.0

            # Substring match (e.g., "date" in "transaction date")
            if normalized_pattern in normalized_source or normalized_source in normalized_pattern:
                best_score = max(best_score, 0.9)

            # Fuzzy string similarity (handles typos, abbreviations)
            # Uses SequenceMatcher from difflib (similar to Levenshtein distance)
            similarity = SequenceMatcher(None, normalized_source, normalized_pattern).ratio()
            best_score = max(best_score, similarity)

        return best_score

    @staticmethod
    def get_mapping_confidence(mappings: dict[str, Optional[str]]) -> float:
        """
        Calculate overall confidence in mapping quality.

        Args:
            mappings: Column mappings dictionary

        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not mappings:
            return 0.0

        mapped_count = sum(1 for val in mappings.values() if val is not None)
        total_count = len(mappings)

        return mapped_count / total_count

    @staticmethod
    def get_required_columns(template_type: str) -> list[str]:
        """
        Get list of required columns for a template type.

        Args:
            template_type: Template type name

        Returns:
            List of required standard column names
        """
        # For MVP, define required columns per template
        # In Phase 2, this will be configurable per tenant
        required_columns = {
            "BankStatement": ["transaction_date", "description"],
            "TrialBalance": ["account_code", "account_name"],
            "AP_OpenItems": ["vendor_name", "invoice_number", "amount"],
            "AR_Aging": ["customer_name", "invoice_number", "amount"],
            "POS_Sales": ["transaction_date", "product_code", "quantity", "total_amount"],
        }

        return required_columns.get(template_type, [])

    @staticmethod
    def validate_mappings(mappings: dict[str, Optional[str]], template_type: str) -> tuple[bool, list[str]]:
        """
        Validate that all required columns are mapped.

        Args:
            mappings: Column mappings dictionary
            template_type: Template type name

        Returns:
            Tuple of (is_valid, missing_columns)
        """
        required_columns = ColumnMapper.get_required_columns(template_type)
        missing_columns = []

        for col in required_columns:
            if col not in mappings or mappings[col] is None:
                missing_columns.append(col)

        is_valid = len(missing_columns) == 0
        return is_valid, missing_columns
