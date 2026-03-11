"""
Quick test script to verify the backend /api/predict endpoint is working
"""
import requests

# Test if backend is running
try:
    # Try a simple GET to check if server is up
    response = requests.get("http://127.0.0.1:8000/api/predict")
    print(f"GET /api/predict status: {response.status_code}")
    if response.status_code == 405:
        print("✅ Backend is running! (405 is expected for GET requests)")
    
    # Now let's check if we can access the docs
    docs_response = requests.get("http://127.0.0.1:8000/docs")
    print(f"\nGET /docs status: {docs_response.status_code}")
    if docs_response.status_code == 200:
        print("✅ FastAPI docs are accessible at http://127.0.0.1:8000/docs")
        print("   You can test the API there!")
    
except requests.exceptions.ConnectionError:
    print("❌ Backend is not running or not accessible")
except Exception as e:
    print(f"❌ Error: {e}")
