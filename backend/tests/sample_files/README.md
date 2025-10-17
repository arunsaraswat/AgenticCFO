# Sample Test Files

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
