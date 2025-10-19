"""Test Excel artifact generation."""
import asyncio
import os
from app.artifacts.excel_generator import generate_cash_ladder

async def test_excel_generation():
    """Test generating a Cash Ladder Excel file."""

    # Test data
    current_cash = 750000.00
    liquidity_warnings = [
        "Cash balance projected to drop below $500K in Week 8",
        "AP aging shows $200K due in next 2 weeks"
    ]
    recommendations = [
        "Accelerate AR collections on past-due invoices",
        "Consider delaying capital expenditures by 1 quarter",
        "Review credit line options as contingency"
    ]
    metadata = {
        "generated_at": "2025-10-18 19:00:00",
        "agent": "cash_commander",
        "tenant_name": "Demo Tenant"
    }

    # Generate Excel (will use sample forecast data)
    output_dir = "/tmp/artifacts"
    os.makedirs(output_dir, exist_ok=True)

    artifact_info = generate_cash_ladder(
        current_cash=current_cash,
        forecast_data=None,  # Will use sample data
        liquidity_warnings=liquidity_warnings,
        recommendations=recommendations,
        metadata=metadata,
        output_dir=output_dir
    )

    print("✓ Excel file generated successfully!")
    print(f"  File path: {artifact_info['file_path']}")
    print(f"  Filename: {artifact_info['filename']}")
    print(f"  Type: {artifact_info['artifact_type']}")
    print(f"  Size: {artifact_info['size_bytes']:,} bytes")
    print(f"  Description: {artifact_info['description']}")

    # Verify file exists
    if os.path.exists(artifact_info['file_path']):
        print(f"✓ File exists at: {artifact_info['file_path']}")
        file_size = os.path.getsize(artifact_info['file_path'])
        print(f"✓ File size: {file_size:,} bytes")

        # Open with system default app (macOS)
        os.system(f"open '{artifact_info['file_path']}'")
    else:
        print(f"✗ File not found at: {artifact_info['file_path']}")

if __name__ == "__main__":
    asyncio.run(test_excel_generation())
