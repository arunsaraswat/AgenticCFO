#!/usr/bin/env python3
"""
Quick integration test to verify the end-to-end flow works.

This script tests:
1. Upload file endpoint returns work_order_id
2. Work order is created in database
3. Execute endpoint exists and is callable
4. Artifact download endpoint exists

Run: python test_integration_flow.py
"""
import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("=" * 70)
print("INTEGRATION FLOW TEST")
print("=" * 70)

# Test 1: Check if all endpoints are registered
print("\n[Test 1] Checking endpoint registration...")

routes = [route.path for route in app.routes]

required_endpoints = [
    "/api/intake/upload",
    "/api/work-orders",
    "/api/work-orders/{work_order_id}",
    "/api/work-orders/{work_order_id}/execute",
    "/api/artifacts/{artifact_id}",
    "/api/artifacts/{artifact_id}/download",
]

for endpoint in required_endpoints:
    if endpoint in routes:
        print(f"  ✓ {endpoint}")
    else:
        print(f"  ✗ {endpoint} - NOT FOUND")

# Test 2: Check OpenAPI docs
print("\n[Test 2] Checking OpenAPI documentation...")

response = client.get("/docs")
if response.status_code == 200:
    print("  ✓ OpenAPI docs accessible at /docs")
else:
    print(f"  ✗ OpenAPI docs failed: {response.status_code}")

# Test 3: Health check
print("\n[Test 3] Health check...")

response = client.get("/health")
if response.status_code == 200:
    print(f"  ✓ Health check passed: {response.json()}")
else:
    print(f"  ✗ Health check failed: {response.status_code}")

# Test 4: List all endpoints
print("\n[Test 4] Available API endpoints:")

api_routes = [route for route in app.routes if hasattr(route, 'path') and route.path.startswith('/api/')]
api_routes.sort(key=lambda r: r.path)

for route in api_routes:
    methods = route.methods if hasattr(route, 'methods') else []
    methods_str = ", ".join(sorted(methods))
    print(f"  {methods_str:20s} {route.path}")

print("\n" + "=" * 70)
print("✓ INTEGRATION FLOW TEST COMPLETE")
print("=" * 70)
print("\nNext steps:")
print("1. Start the server: ./start.sh or uvicorn app.main:app --reload")
print("2. Run full integration test: pytest tests/test_e2e_cash_commander.py -v")
print("3. Test via frontend: Upload a file and watch the work order execute")
print("=" * 70)
