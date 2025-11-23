"""Test security features"""
import requests
import time
from app.utils.password import validate_password

BASE_URL = "http://127.0.0.1:8000"

def test_rate_limiting():
    """Test rate limiting on login endpoint"""
    print("="*50)
    print("TESTING RATE LIMITING")
    print("="*50)
    
    print("\n1. Testing login rate limit (5/minute):")
    success_count = 0
    rate_limited = False
    
    for i in range(7):
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })
        
        if response.status_code == 429:
            rate_limited = True
            print(f"   Attempt {i+1}: Rate limited (429) ✅")
            break
        else:
            print(f"   Attempt {i+1}: {response.status_code}")
            success_count += 1
    
    if rate_limited:
        print("   ✅ Rate limiting working!")
    else:
        print("   ⚠️  Rate limit not triggered (may need more attempts)")

def test_contact_rate_limit():
    """Test rate limiting on contact form"""
    print("\n" + "="*50)
    print("TESTING CONTACT FORM RATE LIMITING")
    print("="*50)
    
    print("\n1. Testing contact rate limit (3/hour):")
    
    for i in range(4):
        response = requests.post(f"{BASE_URL}/api/contact", json={
            "name": f"Test User {i}",
            "email": f"test{i}@example.com",
            "phone": "081234567890",
            "message": "This is a test message for rate limiting"
        })
        
        if response.status_code == 429:
            print(f"   Submission {i+1}: Rate limited (429) ✅")
            print("   ✅ Contact rate limiting working!")
            return
        else:
            print(f"   Submission {i+1}: {response.status_code}")
    
    print("   ⚠️  Rate limit not triggered (may need more submissions)")

def test_password_validation():
    """Test password strength validation"""
    print("\n" + "="*50)
    print("TESTING PASSWORD VALIDATION")
    print("="*50)
    
    test_cases = [
        ("weak", False, "Too short"),
        ("password", False, "Common password"),
        ("Password1", False, "No special character"),
        ("Password!", False, "No number"),
        ("PASSWORD1!", False, "No lowercase"),
        ("password1!", False, "No uppercase"),
        ("Pass123!", True, "Valid strong password"),
        ("MyP@ssw0rd", True, "Valid strong password"),
    ]
    
    for password, should_pass, description in test_cases:
        is_valid, error = validate_password(password)
        status = "✅ PASS" if (is_valid == should_pass) else "❌ FAIL"
        print(f"\n   Password: '{password}'")
        print(f"   Expected: {description}")
        print(f"   Result: {status}")
        if not is_valid:
            print(f"   Error: {error}")

def test_cors_headers():
    """Test CORS configuration"""
    print("\n" + "="*50)
    print("TESTING CORS CONFIGURATION")
    print("="*50)
    
    # Test OPTIONS request
    response = requests.options(f"{BASE_URL}/api/portfolio")
    
    print(f"\n1. CORS Headers:")
    cors_headers = {
        'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
        'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
        'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
    }
    
    for header, value in cors_headers.items():
        if value:
            print(f"   {header}: {value}")
    
    # Check if CORS is properly restricted
    methods = cors_headers.get('Access-Control-Allow-Methods', '')
    if methods and '*' not in methods:
        print("   ✅ CORS methods properly restricted")
    else:
        print("   ⚠️  CORS allows all methods")

def main():
    print("="*50)
    print("SECURITY FEATURES TEST SUITE")
    print("="*50)
    
    try:
        test_password_validation()
        test_rate_limiting()
        test_contact_rate_limit()
        test_cors_headers()
        
        print("\n" + "="*50)
        print("✅ SECURITY TESTS COMPLETED")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
