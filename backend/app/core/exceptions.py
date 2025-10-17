"""Custom exceptions for granular error handling.

These exceptions map to specific HTTP status codes:
- FileValidationError → 422 Unprocessable Entity (file structure/content issues)
- InvalidFileTypeError → 400 Bad Request (wrong file extension)
- FileSizeExceededError → 413 Request Entity Too Large
- TemplateDetectionError → 422 Unprocessable Entity (cannot detect template)
- ColumnMappingError → 422 Unprocessable Entity (cannot map columns)
- DataQualityError → 422 Unprocessable Entity (DQ validation failed)
"""


class FileValidationError(Exception):
    """Raised when file validation fails (structure, content, format issues).

    HTTP Status: 422 Unprocessable Entity
    """
    pass


class InvalidFileTypeError(Exception):
    """Raised when file extension is not allowed.

    HTTP Status: 400 Bad Request
    """
    pass


class FileSizeExceededError(Exception):
    """Raised when file size exceeds maximum allowed.

    HTTP Status: 413 Request Entity Too Large
    """
    pass


class TemplateDetectionError(Exception):
    """Raised when template type cannot be detected from file.

    HTTP Status: 422 Unprocessable Entity
    """
    pass


class ColumnMappingError(Exception):
    """Raised when columns cannot be mapped to template schema.

    HTTP Status: 422 Unprocessable Entity
    """
    pass


class DataQualityError(Exception):
    """Raised when data quality validation fails.

    HTTP Status: 422 Unprocessable Entity
    """
    pass


class FileParseError(Exception):
    """Raised when file cannot be parsed (corrupted, invalid format).

    HTTP Status: 422 Unprocessable Entity
    """
    pass
