import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_agents():
    # 1. Test System Reasoning (Chat)
    print("Testing System Reasoning Agent...")
    query = {"query": "What services are currently in the system?"}
    try:
        response = requests.post(f"{BASE_URL}/query/chat", json=query)
        print(f"Chat Status: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Failed to test chat: {e}")

    # 2. Test Log Debugger
    print("\nTesting Log Debugger Agent...")
    log_data = {
        "log_data": "ERROR: Payment gateway timeout after 30s",
        "context": "Service: payment-service, Timestamp: 2023-10-27T10:00:00Z"
    }
    try:
        response = requests.post(f"{BASE_URL}/query/rootcause", json=log_data)
        print(f"Debugger Status: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Failed to test debugger: {e}")

    # 3. Test Docs Generator
    print("\nTesting Docs Generator Agent...")
    service_data = {
        "service_name": "payment-service",
        "description": "Handles payment processing",
        "metadata": {"language": "python", "framework": "fastapi"}
    }
    try:
        response = requests.post(f"{BASE_URL}/query/docs/generate", json=service_data)
        print(f"Docs Status: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Failed to test docs: {e}")

if __name__ == "__main__":
    # Wait a bit for reload
    time.sleep(2)
    test_agents()
