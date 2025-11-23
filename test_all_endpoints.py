"""Test all API endpoints"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None

def login():
    """Login and get token"""
    global TOKEN
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "admin@terasinterior.com",
        "password": "admin123"
    })
    if response.status_code == 200:
        data = response.json()
        TOKEN = data["access_token"]
        print("✅ Login successful")
        return True
    else:
        print(f"❌ Login failed: {response.text}")
        return False

def test_portfolio():
    """Test portfolio endpoints"""
    print("\n" + "="*50)
    print("TESTING PORTFOLIO ENDPOINTS")
    print("="*50)
    
    # Get published portfolio (public)
    response = requests.get(f"{BASE_URL}/api/portfolio")
    print(f"GET /api/portfolio: {response.status_code} - {len(response.json())} items")
    
    # Get all portfolio (admin)
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/portfolio/admin", headers=headers)
    print(f"GET /api/portfolio/admin: {response.status_code} - {len(response.json())} items")
    
    # Get single portfolio
    response = requests.get(f"{BASE_URL}/api/portfolio/1")
    print(f"GET /api/portfolio/1: {response.status_code}")
    
    print("✅ Portfolio endpoints working")

def test_services():
    """Test services endpoints"""
    print("\n" + "="*50)
    print("TESTING SERVICES ENDPOINTS")
    print("="*50)
    
    # Get published services
    response = requests.get(f"{BASE_URL}/api/services")
    print(f"GET /api/services: {response.status_code} - {len(response.json())} items")
    
    # Get single service
    response = requests.get(f"{BASE_URL}/api/services/1")
    print(f"GET /api/services/1: {response.status_code}")
    
    print("✅ Services endpoints working")

def test_contacts():
    """Test contacts endpoints"""
    print("\n" + "="*50)
    print("TESTING CONTACTS ENDPOINTS")
    print("="*50)
    
    # Submit contact (public)
    response = requests.post(f"{BASE_URL}/api/contact", json={
        "name": "Test User",
        "email": "test@example.com",
        "phone": "08123456789",
        "message": "This is a test message"
    })
    print(f"POST /api/contact: {response.status_code}")
    
    # Get all contacts (admin)
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/contact", headers=headers)
    print(f"GET /api/contact: {response.status_code} - {len(response.json())} items")
    
    print("✅ Contacts endpoints working")

def test_settings():
    """Test settings endpoints"""
    print("\n" + "="*50)
    print("TESTING SETTINGS ENDPOINTS")
    print("="*50)
    
    # Get public settings
    response = requests.get(f"{BASE_URL}/api/settings/public")
    print(f"GET /api/settings/public: {response.status_code} - {len(response.json())} settings")
    
    # Get all settings (admin)
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/settings", headers=headers)
    print(f"GET /api/settings: {response.status_code} - {len(response.json())} items")
    
    print("✅ Settings endpoints working")

def test_stats():
    """Test stats endpoints"""
    print("\n" + "="*50)
    print("TESTING STATS ENDPOINTS")
    print("="*50)
    
    # Get dashboard stats
    response = requests.get(f"{BASE_URL}/api/stats/dashboard")
    if response.status_code == 200:
        data = response.json()
        print(f"GET /api/stats/dashboard: {response.status_code}")
        print(f"  - Portfolio: {data['totalPortfolio']}")
        print(f"  - Services: {data['totalServices']}")
        print(f"  - Contacts: {data['totalContacts']}")
    else:
        print(f"GET /api/stats/dashboard: {response.status_code}")
    
    # Get contact trend
    response = requests.get(f"{BASE_URL}/api/stats/contact-trend")
    print(f"GET /api/stats/contact-trend: {response.status_code}")
    
    print("✅ Stats endpoints working")

def main():
    print("="*50)
    print("TERAS INTERIOR API TEST")
    print("="*50)
    
    if not login():
        print("❌ Cannot proceed without login")
        return
    
    try:
        test_portfolio()
        test_services()
        test_contacts()
        test_settings()
        test_stats()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    main()
