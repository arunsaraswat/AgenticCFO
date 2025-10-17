"""Quick manual test for file upload flow."""
import requests
import json
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
SAMPLE_FILES_DIR = Path(__file__).parent / "sample_files"

# Test credentials (you may need to register a user first)
TEST_USER = {
    "email": "test@agenticcfo.com",
    "password": "TestPassword123!"
}

def test_upload_flow():
    """Test the complete upload flow."""

    print("=" * 60)
    print("Testing File Upload Flow")
    print("=" * 60)

    # Step 1: Register/Login
    print("\n1. Authenticating...")

    # Try to login first
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
    )

    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        print(f"   ✓ Logged in successfully")
    else:
        # Try to register
        print("   → Login failed, attempting registration...")
        register_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"],
                "full_name": "Test User"
            }
        )

        if register_response.status_code == 201:
            print(f"   ✓ Registered successfully")
            # Now login
            login_response = requests.post(
                f"{BASE_URL}/api/auth/login",
                data={
                    "username": TEST_USER["email"],
                    "password": TEST_USER["password"]
                }
            )
            token = login_response.json()["access_token"]
        else:
            print(f"   ✗ Registration failed: {register_response.text}")
            return

    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Upload BankStatement
    print("\n2. Uploading BankStatement.xlsx...")
    bank_file_path = SAMPLE_FILES_DIR / "BankStatement.xlsx"

    if not bank_file_path.exists():
        print(f"   ✗ File not found: {bank_file_path}")
        return

    with open(bank_file_path, "rb") as f:
        files = {"file": ("BankStatement.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        upload_response = requests.post(
            f"{BASE_URL}/api/intake/upload",
            headers=headers,
            files=files
        )

    if upload_response.status_code == 201:
        upload_data = upload_response.json()
        print(f"   ✓ Upload successful!")
        print(f"   → File ID: {upload_data['id']}")
        print(f"   → Status: {upload_data['status']}")
        print(f"   → File Hash: {upload_data['file_hash'][:16]}...")

        file_upload_id = upload_data['id']
    else:
        print(f"   ✗ Upload failed: {upload_response.status_code}")
        print(f"   → Response: {upload_response.text}")
        return

    # Step 3: Process the file (parse + template detection)
    print("\n3. Processing file...")
    process_response = requests.post(
        f"{BASE_URL}/api/intake/{file_upload_id}/process",
        headers=headers
    )

    if process_response.status_code == 200:
        process_data = process_response.json()
        print(f"   ✓ Processing successful!")
        print(f"   → Template Type: {process_data.get('template_type', 'N/A')}")
        print(f"   → Total Rows: {process_data.get('total_rows', 'N/A')}")
        print(f"   → Dataset ID: {process_data.get('dataset_id', 'N/A')}")

        if 'dq_results' in process_data:
            dq = process_data['dq_results']
            print(f"   → DQ Status: {dq.get('status', 'N/A')}")
            if dq.get('errors'):
                print(f"   → Errors: {len(dq['errors'])}")
            if dq.get('warnings'):
                print(f"   → Warnings: {len(dq['warnings'])}")
    else:
        print(f"   ✗ Processing failed: {process_response.status_code}")
        print(f"   → Response: {process_response.text}")
        return

    # Step 4: Upload TrialBalance
    print("\n4. Uploading TrialBalance.xlsx...")
    trial_file_path = SAMPLE_FILES_DIR / "TrialBalance.xlsx"

    with open(trial_file_path, "rb") as f:
        files = {"file": ("TrialBalance.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        upload_response = requests.post(
            f"{BASE_URL}/api/intake/upload",
            headers=headers,
            files=files
        )

    if upload_response.status_code == 201:
        upload_data = upload_response.json()
        print(f"   ✓ Upload successful!")
        print(f"   → File ID: {upload_data['id']}")

        # Process it
        file_upload_id = upload_data['id']
        process_response = requests.post(
            f"{BASE_URL}/api/intake/{file_upload_id}/process",
            headers=headers
        )

        if process_response.status_code == 200:
            process_data = process_response.json()
            print(f"   ✓ Processing successful!")
            print(f"   → Template Type: {process_data.get('template_type', 'N/A')}")

    print("\n" + "=" * 60)
    print("✅ Upload flow test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_upload_flow()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to backend server.")
        print("  Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
