import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_ingest():
    # 1. Ingest Manifest
    manifest = {
        "name": "payment-service",
        "description": "Handles payment processing",
        "repo_url": "github.com/org/payment-service",
        "metadata": {"language": "python", "version": "1.0.0"}
    }
    print("Ingesting manifest...")
    try:
        response = requests.post(f"{BASE_URL}/ingest/manifest", json=manifest)
        print(f"Manifest Status: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Failed to ingest manifest: {e}")
        return

    # 2. Ingest Logs
    logs = [
        {
            "service_name": "payment-service",
            "level": "INFO",
            "message": "Payment processed successfully",
            "context": {"amount": 100, "currency": "USD"}
        },
        {
            "service_name": "payment-service",
            "level": "ERROR",
            "message": "Payment gateway timeout",
            "context": {"error_code": "TIMEOUT"}
        }
    ]
    print("\nIngesting logs...")
    try:
        response = requests.post(f"{BASE_URL}/ingest/logs", json=logs)
        print(f"Logs Status: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Failed to ingest logs: {e}")

if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server...")
    time.sleep(5) 
    test_ingest()
