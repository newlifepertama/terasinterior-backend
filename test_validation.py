"""Test input validation"""
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_contact_validation():
    """Test contact form validation"""
    print("="*50)
    print("TESTING CONTACT VALIDATION")
    print("="*50)
    
    # Test 1: Valid contact
    print("\n1. Valid contact:")
    response = requests.post(f"{BASE_URL}/api/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "081234567890",
        "message": "This is a valid test message with enough characters"
    })
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 201 else '❌ FAIL'}")
    
    # Test 2: Name too short
    print("\n2. Name too short (should fail):")
    response = requests.post(f"{BASE_URL}/api/contact", json={
        "name": "A",
        "email": "test@example.com",
        "phone": "081234567890",
        "message": "This is a test message"
    })
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 422 else '❌ FAIL'}")
    
    # Test 3: Invalid email
    print("\n3. Invalid email (should fail):")
    response = requests.post(f"{BASE_URL}/api/contact", json={
        "name": "John Doe",
        "email": "invalid-email",
        "phone": "081234567890",
        "message": "This is a test message"
    })
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 422 else '❌ FAIL'}")
    
    # Test 4: Message too short
    print("\n4. Message too short (should fail):")
    response = requests.post(f"{BASE_URL}/api/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "081234567890",
        "message": "Short"
    })
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 422 else '❌ FAIL'}")
    
    # Test 5: XSS attempt (should be sanitized)
    print("\n5. XSS attempt (should be sanitized):")
    response = requests.post(f"{BASE_URL}/api/contact", json={
        "name": "<script>alert('xss')</script>John",
        "email": "john@example.com",
        "phone": "081234567890",
        "message": "Test message with <script>alert('xss')</script> injection attempt"
    })
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        has_script = '<script>' in data['name'] or '<script>' in data['message']
        print(f"   XSS Blocked: {'✅ PASS' if not has_script else '❌ FAIL'}")

def test_portfolio_validation():
    """Test portfolio validation"""
    print("\n" + "="*50)
    print("TESTING PORTFOLIO VALIDATION")
    print("="*50)
    
    # Login first
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "admin@terasinterior.com",
        "password": "admin123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Valid portfolio
    print("\n1. Valid portfolio:")
    response = requests.post(f"{BASE_URL}/api/portfolio", 
        headers=headers,
        json={
            "title": "Test Portfolio",
            "description": "This is a test description",
            "category": "Residential",
            "image_url": "https://example.com/image.jpg",
            "published": False,
            "order_index": 0
        }
    )
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 201 else '❌ FAIL'}")
    
    # Test 2: Invalid URL
    print("\n2. Invalid image URL (should fail):")
    response = requests.post(f"{BASE_URL}/api/portfolio",
        headers=headers,
        json={
            "title": "Test Portfolio",
            "description": "Test",
            "category": "Residential",
            "image_url": "not-a-valid-url",
            "published": False
        }
    )
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 422 else '❌ FAIL'}")
    
    # Test 3: Title too short
    print("\n3. Title too short (should fail):")
    response = requests.post(f"{BASE_URL}/api/portfolio",
        headers=headers,
        json={
            "title": "AB",
            "category": "Residential",
            "image_url": "https://example.com/image.jpg"
        }
    )
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 422 else '❌ FAIL'}")

def test_request_size_limit():
    """Test request size limit"""
    print("\n" + "="*50)
    print("TESTING REQUEST SIZE LIMIT")
    print("="*50)
    
    # Create a large payload (>10MB)
    print("\n1. Large request (>10MB, should fail):")
    large_message = "A" * (11 * 1024 * 1024)  # 11MB
    response = requests.post(f"{BASE_URL}/api/contact", json={
        "name": "Test",
        "email": "test@example.com",
        "message": large_message
    })
    print(f"   Status: {response.status_code} - {'✅ PASS' if response.status_code == 413 else '❌ FAIL'}")

def main():
    print("="*50)
    print("INPUT VALIDATION TEST SUITE")
    print("="*50)
    
    try:
        test_contact_validation()
        test_portfolio_validation()
        test_request_size_limit()
        
        print("\n" + "="*50)
        print("✅ VALIDATION TESTS COMPLETED")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    main()
