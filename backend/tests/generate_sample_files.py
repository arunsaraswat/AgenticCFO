"""Generate sample Excel files for testing the file intake system."""
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Create output directory
output_dir = Path(__file__).parent / "sample_files"
output_dir.mkdir(exist_ok=True)

print(f"Generating sample files in: {output_dir}")

# 1. Bank Statement (for Cash Commander)
print("\n1. Creating BankStatement.xlsx...")
bank_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
bank_data = {
    "Date": bank_dates,
    "Description": [
        "Customer Payment - ABC Corp",
        "Vendor Payment - XYZ Supplies",
        "Wire Transfer In",
        "Payroll Processing",
        "Customer Payment - DEF Inc",
        "Rent Payment",
        "Utility Bill",
        "Customer Payment - GHI Ltd",
        "Vendor Payment - Office Depot",
        "Interest Income",
        "Customer Payment - JKL Corp",
        "Insurance Payment",
        "Vendor Payment - Tech Supplies",
        "Customer Payment - MNO Inc",
        "Tax Payment",
        "Customer Payment - PQR Ltd",
        "Vendor Payment - Maintenance",
        "Wire Transfer In",
        "Customer Payment - STU Corp",
        "Vendor Payment - Shipping Co",
        "Customer Payment - VWX Inc",
        "Office Supplies",
        "Customer Payment - YZA Ltd",
        "Vendor Payment - Consulting",
        "Customer Payment - BCD Corp",
        "Equipment Lease",
        "Customer Payment - EFG Inc",
        "Vendor Payment - Marketing",
        "Customer Payment - HIJ Ltd",
        "Wire Transfer In",
    ],
    "Debit": [
        None, 5200.00, None, 125000.00, None, 15000.00, 2800.00, None, 3500.00, None,
        None, 8500.00, 4200.00, None, 35000.00, None, 2100.00, None, None, 6800.00,
        None, 1500.00, None, 12000.00, None, 7500.00, None, 8900.00, None, None
    ],
    "Credit": [
        45000.00, None, 75000.00, None, 32000.00, None, None, 28000.00, None, 450.00,
        19000.00, None, None, 41000.00, None, 23000.00, None, 55000.00, 36000.00, None,
        27000.00, None, 31000.00, None, 38000.00, None, 29000.00, None, 33000.00, 62000.00
    ],
    "Balance": [
        485000.00, 479800.00, 554800.00, 429800.00, 461800.00, 446800.00, 444000.00, 472000.00, 468500.00, 468950.00,
        487950.00, 479450.00, 475250.00, 516250.00, 481250.00, 504250.00, 502150.00, 557150.00, 593150.00, 586350.00,
        613350.00, 611850.00, 642850.00, 630850.00, 668850.00, 661350.00, 690350.00, 681450.00, 714450.00, 776450.00
    ]
}
bank_df = pd.DataFrame(bank_data)
bank_df.to_excel(output_dir / "BankStatement.xlsx", index=False, sheet_name="Transactions")
print(f"   ✓ Created with {len(bank_df)} transactions, ending balance: ${bank_df['Balance'].iloc[-1]:,.2f}")

# 2. Trial Balance (for Close Copilot)
print("\n2. Creating TrialBalance.xlsx...")
trial_balance_data = {
    "Account_Code": [
        "1010", "1020", "1200", "1500", "1600", "1700",
        "2010", "2020", "2100", "2200",
        "3010", "3020",
        "4010", "4020",
        "5010", "5020", "5030", "6010", "6020", "7010"
    ],
    "Account_Name": [
        "Cash - Operating", "Cash - Payroll", "Accounts Receivable", "Inventory", "Prepaid Expenses", "Fixed Assets",
        "Accounts Payable", "Accrued Expenses", "Notes Payable - Short Term", "Notes Payable - Long Term",
        "Common Stock", "Retained Earnings",
        "Revenue - Products", "Revenue - Services",
        "COGS - Materials", "COGS - Labor", "COGS - Overhead", "Operating Expenses", "Depreciation", "Interest Expense"
    ],
    "Debit": [
        776450.00, 125000.00, 845000.00, 1250000.00, 45000.00, 2500000.00,
        None, None, None, None,
        None, None,
        None, None,
        750000.00, 425000.00, 180000.00, 685000.00, 125000.00, 48000.00
    ],
    "Credit": [
        None, None, None, None, None, None,
        425000.00, 95000.00, 350000.00, 1200000.00,
        500000.00, 1250000.00,
        2850000.00, 950000.00,
        None, None, None, None, None, None
    ],
    "Balance": [
        776450.00, 125000.00, 845000.00, 1250000.00, 45000.00, 2500000.00,
        -425000.00, -95000.00, -350000.00, -1200000.00,
        -500000.00, -1250000.00,
        -2850000.00, -950000.00,
        750000.00, 425000.00, 180000.00, 685000.00, 125000.00, 48000.00
    ]
}
trial_balance_df = pd.DataFrame(trial_balance_data)
trial_balance_df.to_excel(output_dir / "TrialBalance.xlsx", index=False, sheet_name="Trial Balance")
print(f"   ✓ Created with {len(trial_balance_df)} accounts")
print(f"   ✓ Total Debits: ${trial_balance_df['Debit'].sum():,.2f}")
print(f"   ✓ Total Credits: ${trial_balance_df['Credit'].sum():,.2f}")

# 3. AR Open Items (for Cash Commander forecasting)
print("\n3. Creating AR_OpenItems.xlsx...")
ar_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(90, 0, -15)]
ar_due_dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 90, 15)]
ar_data = {
    "Invoice_Number": ["INV-2024-001", "INV-2024-002", "INV-2024-003", "INV-2024-004", "INV-2024-005", "INV-2024-006"],
    "Customer_Name": ["ABC Corp", "DEF Inc", "GHI Ltd", "JKL Corp", "MNO Inc", "PQR Ltd"],
    "Invoice_Date": ar_dates,
    "Due_Date": ar_due_dates,
    "Amount": [125000.00, 87000.00, 210000.00, 65000.00, 145000.00, 98000.00],
    "Days_Outstanding": [90, 75, 60, 45, 30, 15],
    "Status": ["Overdue", "Overdue", "Overdue", "Current", "Current", "Current"]
}
ar_df = pd.DataFrame(ar_data)
ar_df.to_excel(output_dir / "AR_OpenItems.xlsx", index=False, sheet_name="Open Items")
print(f"   ✓ Created with {len(ar_df)} open invoices, total AR: ${ar_df['Amount'].sum():,.2f}")

# 4. AP Open Items (for Cash Commander forecasting)
print("\n4. Creating AP_OpenItems.xlsx...")
ap_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(60, 0, -10)]
ap_due_dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 60, 10)]
ap_data = {
    "Invoice_Number": ["VNDR-001", "VNDR-002", "VNDR-003", "VNDR-004", "VNDR-005", "VNDR-006"],
    "Vendor_Name": ["XYZ Supplies", "Office Depot", "Tech Supplies", "Maintenance Co", "Shipping Co", "Consulting Inc"],
    "Invoice_Date": ap_dates,
    "Due_Date": ap_due_dates,
    "Amount": [52000.00, 35000.00, 42000.00, 21000.00, 68000.00, 120000.00],
    "Days_Until_Due": [0, 10, 20, 30, 40, 50],
    "Payment_Terms": ["Net 30", "Net 30", "Net 45", "Net 30", "Net 60", "Net 30"]
}
ap_df = pd.DataFrame(ap_data)
ap_df.to_excel(output_dir / "AP_OpenItems.xlsx", index=False, sheet_name="Open Items")
print(f"   ✓ Created with {len(ap_df)} open invoices, total AP: ${ap_df['Amount'].sum():,.2f}")

# 5. Create a README
print("\n5. Creating README.md...")
readme_content = """# Sample Test Files

These files are used for testing the Agentic CFO file intake system.

## Files

### BankStatement.xlsx
- **Purpose:** Test bank transaction parsing for Cash Commander agent
- **Columns:** Date, Description, Debit, Credit, Balance
- **Rows:** 30 days of transactions
- **Template Type:** `BankStatement`

### TrialBalance.xlsx
- **Purpose:** Test trial balance parsing for Close Copilot agent
- **Columns:** Account_Code, Account_Name, Debit, Credit, Balance
- **Rows:** 20 accounts across Assets, Liabilities, Equity, Revenue, Expenses
- **Template Type:** `TrialBalance`

### AR_OpenItems.xlsx
- **Purpose:** Test AR aging for cash forecasting
- **Columns:** Invoice_Number, Customer_Name, Invoice_Date, Due_Date, Amount, Days_Outstanding, Status
- **Rows:** 6 open invoices (mix of current and overdue)
- **Template Type:** `AR_OpenItems`

### AP_OpenItems.xlsx
- **Purpose:** Test AP aging for cash forecasting
- **Columns:** Invoice_Number, Vendor_Name, Invoice_Date, Due_Date, Amount, Days_Until_Due, Payment_Terms
- **Rows:** 6 open invoices with various due dates
- **Template Type:** `AP_OpenItems`

## Usage

These files can be uploaded via the `/api/intake/upload` endpoint for testing.

## Regeneration

Run `python generate_sample_files.py` to regenerate all sample files with current dates.
"""
with open(output_dir / "README.md", "w") as f:
    f.write(readme_content)
print("   ✓ Created README.md")

print("\n" + "="*60)
print("✅ All sample files generated successfully!")
print(f"📁 Location: {output_dir}")
print("="*60)
