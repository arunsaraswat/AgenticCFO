# Artifact Generation Module

This module handles the generation of financial artifacts in various formats (Excel, PDF, Word) from agent outputs.

## Overview

Agents process financial data and generate structured outputs. These outputs need to be converted into professional, formatted artifacts that users can download and share. This module provides generators for common artifact types.

## Available Generators

### Excel Generator (`excel_generator.py`)

Generates professional Excel workbooks for financial reports.

#### Features

- **Cash Ladder Generator**: 13-week rolling cash forecast
  - Professional formatting with headers, colors, borders
  - Currency formatting ($#,##0.00)
  - Conditional formatting (low balance warnings in red)
  - Automatic totals with Excel formulas
  - Liquidity warnings section
  - Recommended actions section
  - Key metrics summary

#### Usage

```python
from app.artifacts.excel_generator import generate_cash_ladder

# Generate Cash Ladder
result = generate_cash_ladder(
    current_cash=1245678.90,
    forecast_data=[
        {
            "week_number": 1,
            "week_ending": "2024-10-24",
            "beginning_balance": 1245678.90,
            "cash_receipts": 280000.00,
            "cash_disbursements": 185000.00,
            "ending_balance": 1340678.90,
        },
        # ... more weeks
    ],
    liquidity_warnings=[
        "Cash balance falls below minimum threshold in Week 8",
    ],
    recommendations=[
        "Accelerate AR collections",
        "Defer non-critical AP payments",
    ],
    metadata={
        "generated_at": "2024-10-17 14:30:00",
        "tenant_name": "Demo Company Inc.",
        "agent": "cash_commander",
    },
    output_dir="/tmp/artifacts"
)

# Result contains:
# {
#     "file_path": "/tmp/artifacts/Cash_Ladder_abc123.xlsx",
#     "filename": "Cash_Ladder_abc123.xlsx",
#     "artifact_type": "excel",
#     "description": "13-week cash forecast ladder",
#     "size_bytes": 6471
# }
```

#### Forecast Data Schema

Each week in `forecast_data` should contain:

```python
{
    "week_number": int,          # 1-13
    "week_ending": str,          # "YYYY-MM-DD"
    "beginning_balance": float,
    "cash_receipts": float,
    "cash_disbursements": float,
    "ending_balance": float,
}
```

#### Sample Output

The generated Cash Ladder Excel includes:

1. **Header Section**
   - Title: "13-Week Cash Forecast"
   - Metadata: Generated timestamp, tenant name

2. **Current Cash Position**
   - Bold, larger font
   - Currency formatted

3. **Forecast Table**
   - Column headers with blue background
   - 13 rows of weekly data
   - Currency formatting on all monetary columns
   - Borders and alignment
   - Total row with SUM formulas

4. **Conditional Formatting**
   - Ending balances < $500K highlighted in red

5. **Liquidity Warnings** (if any)
   - Red header bar
   - Bulleted list of warnings

6. **Recommended Actions** (if any)
   - Green header bar
   - Bulleted list of recommendations

7. **Key Metrics**
   - Minimum forecasted balance
   - Week of minimum balance

## File Naming Convention

All generated artifacts use UUID-based filenames to ensure uniqueness:

```
{ArtifactType}_{UUID8}.{extension}

Examples:
- Cash_Ladder_a1b2c3d4.xlsx
- GM_Bridge_e5f6g7h8.xlsx
- Covenant_Report_i9j0k1l2.pdf
```

## Output Directory

Artifacts are stored in the directory specified by:

1. `output_dir` parameter (if provided)
2. `ARTIFACTS_STORAGE_PATH` environment variable
3. Default: `/tmp/artifacts`

**Production Setup:**
```bash
# Set in .env
ARTIFACTS_STORAGE_PATH=/var/agenticcfo/artifacts
```

## Testing

### Unit Tests

```bash
cd backend
pytest tests/test_artifacts/test_excel_generator.py -v
```

### Integration Test

```bash
cd backend
python test_artifact_generation.py
```

This runs a standalone test that:
- Generates 13-week forecast data
- Creates Excel artifact
- Validates all sections and formatting
- Reports 9/9 tests passing

## Future Generators (Planned)

### PDF Generator (`pdf_generator.py`)
- Liquidity warnings report
- Covenant compliance report
- Investment memos

### Word Generator (`word_generator.py`)
- Board memo templates
- Executive summaries
- Deal analysis documents

## Architecture Integration

### Agent Workflow

```
Agent.execute()
  → Agent._parse_output()  # Extract structured data
  → Agent._generate_artifacts()  # Call generator
  → Excel/PDF/Word file created
  → Artifact metadata returned
  → Stored in artifacts table (database)
```

### Database Schema

```sql
CREATE TABLE artifacts (
    id UUID PRIMARY KEY,
    work_order_id UUID REFERENCES work_orders(id),
    artifact_type VARCHAR(50),  -- "excel", "pdf", "word"
    filename VARCHAR(255),
    file_path TEXT,
    checksum_sha256 VARCHAR(64),
    size_bytes INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoint

```
GET /api/artifacts/{artifact_id}/download
  → Streams file with proper Content-Type
  → Sets Content-Disposition header for download
```

## Error Handling

Generators include comprehensive error handling:

```python
try:
    artifact = generate_cash_ladder(...)
except Exception as e:
    # Returns error artifact
    return [{
        "artifact_type": "error",
        "filename": "cash_ladder_error.txt",
        "description": f"Failed to generate: {str(e)}",
        "error": str(e)
    }]
```

## Performance

- **Cash Ladder generation time:** ~100-200ms
- **File size:** 6-7 KB for 13-week forecast
- **Memory usage:** Minimal (openpyxl streams to disk)

## Dependencies

```
openpyxl==3.1.2  # Excel generation
```

Future additions:
```
reportlab  # PDF generation
python-docx  # Word generation
```

## Examples

See:
- `backend/test_artifact_generation.py` - Standalone example
- `backend/tests/test_artifacts/test_excel_generator.py` - All test cases
- `backend/app/agents/treasury/cash_commander.py` - Agent integration

## Contributing

When adding new artifact generators:

1. Create generator file in `app/artifacts/`
2. Follow naming convention: `{format}_generator.py`
3. Implement error handling
4. Use UUID-based filenames
5. Return standardized metadata dict
6. Add comprehensive unit tests
7. Add integration test
8. Update this README

## License

Part of the Agentic CFO Platform project.
