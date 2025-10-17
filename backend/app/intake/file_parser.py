"""File parsing utilities for Excel and CSV files.

Handles reading Excel (.xlsx, .xls) and CSV files into pandas DataFrames
with proper error handling and validation.
"""
from pathlib import Path
from typing import Optional

import pandas as pd

from app.core.exceptions import FileParseError


class FileParser:
    """
    Parser for Excel and CSV files.

    Provides a unified interface for reading different file formats
    with consistent error handling.
    """

    # Supported file extensions
    EXCEL_EXTENSIONS = {".xlsx", ".xls"}
    CSV_EXTENSIONS = {".csv"}
    SUPPORTED_EXTENSIONS = EXCEL_EXTENSIONS | CSV_EXTENSIONS

    @staticmethod
    def parse_file(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Parse Excel or CSV file into DataFrame.

        Args:
            file_path: Path to file
            sheet_name: Excel sheet name (optional, defaults to first sheet)

        Returns:
            Pandas DataFrame with parsed data

        Raises:
            FileParseError: If file cannot be parsed
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = path.suffix.lower()

        if file_ext not in FileParser.SUPPORTED_EXTENSIONS:
            raise FileParseError(
                f"Unsupported file extension: {file_ext}. "
                f"Supported: {', '.join(FileParser.SUPPORTED_EXTENSIONS)}"
            )

        try:
            if file_ext in FileParser.EXCEL_EXTENSIONS:
                return FileParser._parse_excel(file_path, sheet_name)
            elif file_ext in FileParser.CSV_EXTENSIONS:
                return FileParser._parse_csv(file_path)
            else:
                raise FileParseError(f"Unsupported file type: {file_ext}")

        except FileParseError:
            raise
        except Exception as e:
            raise FileParseError(f"Failed to parse file: {str(e)}") from e

    @staticmethod
    def _parse_excel(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Parse Excel file.

        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name (None = first sheet)

        Returns:
            DataFrame with parsed data

        Raises:
            FileParseError: If parsing fails
        """
        try:
            # Read Excel file
            # sheet_name=0 means first sheet, sheet_name=None reads all sheets
            df = pd.read_excel(file_path, sheet_name=sheet_name or 0, engine="openpyxl")

            # Validate DataFrame
            if df.empty:
                raise FileParseError("Excel file is empty")

            # Clean column names (remove leading/trailing spaces)
            df.columns = df.columns.str.strip()

            # Drop completely empty rows
            df = df.dropna(how="all")

            # Reset index after dropping rows
            df = df.reset_index(drop=True)

            return df

        except pd.errors.EmptyDataError:
            raise FileParseError("Excel file is empty")
        except Exception as e:
            raise FileParseError(f"Failed to parse Excel file: {str(e)}") from e

    @staticmethod
    def _parse_csv(file_path: str) -> pd.DataFrame:
        """
        Parse CSV file with automatic delimiter detection.

        Args:
            file_path: Path to CSV file

        Returns:
            DataFrame with parsed data

        Raises:
            FileParseError: If parsing fails
        """
        try:
            # Try common delimiters
            delimiters = [",", ";", "\t", "|"]

            for delimiter in delimiters:
                try:
                    df = pd.read_csv(file_path, delimiter=delimiter, engine="python")

                    # Check if we got meaningful data (more than 1 column)
                    if len(df.columns) > 1:
                        # Clean column names
                        df.columns = df.columns.str.strip()

                        # Drop completely empty rows
                        df = df.dropna(how="all")

                        # Reset index
                        df = df.reset_index(drop=True)

                        if not df.empty:
                            return df

                except Exception:
                    continue

            # If we get here, no delimiter worked
            raise FileParseError(
                "Could not parse CSV file. Tried delimiters: " + ", ".join(delimiters)
            )

        except FileParseError:
            raise
        except pd.errors.EmptyDataError:
            raise FileParseError("CSV file is empty")
        except Exception as e:
            raise FileParseError(f"Failed to parse CSV file: {str(e)}") from e

    @staticmethod
    def get_excel_sheet_names(file_path: str) -> list[str]:
        """
        Get list of sheet names in Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            List of sheet names

        Raises:
            FileParseError: If file cannot be read
        """
        try:
            excel_file = pd.ExcelFile(file_path, engine="openpyxl")
            return excel_file.sheet_names
        except Exception as e:
            raise FileParseError(f"Failed to read Excel sheet names: {str(e)}") from e

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, min_rows: int = 1, min_cols: int = 1) -> tuple[bool, Optional[str]]:
        """
        Validate DataFrame meets minimum requirements.

        Args:
            df: DataFrame to validate
            min_rows: Minimum number of rows required
            min_cols: Minimum number of columns required

        Returns:
            Tuple of (is_valid, error_message)
        """
        if df.empty:
            return False, "DataFrame is empty"

        if len(df) < min_rows:
            return False, f"DataFrame has only {len(df)} rows, minimum {min_rows} required"

        if len(df.columns) < min_cols:
            return False, f"DataFrame has only {len(df.columns)} columns, minimum {min_cols} required"

        # Check for unnamed columns (typically means parsing error)
        unnamed_cols = [col for col in df.columns if str(col).startswith("Unnamed:")]
        if len(unnamed_cols) > len(df.columns) / 2:
            return False, "More than 50% of columns are unnamed - possible parsing error"

        return True, None

    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        Get summary information about file without fully parsing it.

        Args:
            file_path: Path to file

        Returns:
            Dictionary with file information
        """
        path = Path(file_path)
        file_ext = path.suffix.lower()

        info = {
            "file_path": str(path),
            "file_name": path.name,
            "file_extension": file_ext,
            "file_size_bytes": path.stat().st_size,
        }

        try:
            if file_ext in FileParser.EXCEL_EXTENSIONS:
                df = FileParser.parse_file(file_path)
                info["row_count"] = len(df)
                info["column_count"] = len(df.columns)
                info["columns"] = df.columns.tolist()
                info["sheet_names"] = FileParser.get_excel_sheet_names(file_path)
            elif file_ext in FileParser.CSV_EXTENSIONS:
                df = FileParser.parse_file(file_path)
                info["row_count"] = len(df)
                info["column_count"] = len(df.columns)
                info["columns"] = df.columns.tolist()
            else:
                info["error"] = f"Unsupported file type: {file_ext}"

        except Exception as e:
            info["error"] = str(e)

        return info
