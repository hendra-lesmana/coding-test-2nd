#!/usr/bin/env python3
"""
Simple test script to verify the RAG system setup
"""

import os
import sys
import requests
import time

def test_backend_health():
    """Test if backend is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend is not accessible: {e}")
        return False

def test_frontend_health():
    """Test if frontend is running"""
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend is not accessible: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    try:
        # Test documents endpoint
        response = requests.get("http://localhost:8000/api/documents", timeout=5)
        if response.status_code == 200:
            print("✅ Documents API endpoint is working")
        else:
            print(f"❌ Documents API returned status code: {response.status_code}")
            
        # Test API documentation
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation is accessible")
        else:
            print(f"❌ API documentation returned status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API endpoints test failed: {e}")

def main():
    print("🧪 Testing RAG-based Financial Q&A System Setup")
    print("=" * 50)
    
    print("\n1. Testing Backend Health...")
    backend_ok = test_backend_health()
    
    print("\n2. Testing Frontend Health...")
    frontend_ok = test_frontend_health()
    
    print("\n3. Testing API Endpoints...")
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok:
        print("🎉 System is ready! You can start using the application.")
        print("📝 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
    else:
        print("⚠️  Some services are not running properly.")
        print("Please check the startup logs and ensure both backend and frontend are running.")

if __name__ == "__main__":
    main()
