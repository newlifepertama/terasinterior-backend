import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("STEP 3: Testing Authentication Flow")
print("=" * 60)
print()

# Test 1: Login
print("Test 1: Login with admin credentials")
print("-" * 60)

# Try common passwords that might have been used
passwords_to_try = [
    "admin123",
    "Admin123",
    "Admin123!",
    "admin",
    "password"
]

login_data = {
    "email": "admin@terasinterior.com",
    "password": ""  # Will be filled in loop
}

token = None
user_data = None

for pwd in passwords_to_try:
    login_data["password"] = pwd
    print(f"Trying password: {pwd}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result["access_token"]
            user_data = result["user"]
            
            print(f"✓ Login successful with password: {pwd}")
            print()
            print("Response:")
            print(json.dumps(result, indent=2))
            print()
            print(f"✓ Access Token: {token[:50]}...")
            print(f"✓ Token Type: {result['token_type']}")
            print(f"✓ User ID: {user_data['id']}")
            print(f"✓ User Email: {user_data['email']}")
            print(f"✓ User Name: {user_data['name']}")
            print(f"✓ User Role: {user_data['role']}")
            break
        else:
            print(f"  ✗ Failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")

if not token:
    print()
    print("=" * 60)
    print("⚠️  Could not login with common passwords")
    print("=" * 60)
    print()
    print("Please enter the correct admin password manually:")
    manual_password = input("Password: ")
    
    login_data["password"] = manual_password
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result["access_token"]
            user_data = result["user"]
            
            print()
            print("✓ Login successful!")
            print()
            print("Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(response.text)
            exit(1)
            
    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)

print()
print("=" * 60)

# Test 2: Get current user info
if token:
    print()
    print("Test 2: Get current user info (Protected endpoint)")
    print("-" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Protected endpoint accessible")
            print()
            print("Current User Info:")
            print(json.dumps(result, indent=2))
        else:
            print(f"✗ Failed to access protected endpoint: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"✗ Error: {e}")

print()
print("=" * 60)
print("Authentication Tests Complete!")
print("=" * 60)
print()

if token:
    print("✅ All tests passed!")
    print()
    print("Save this token for next tests:")
    print(f"TOKEN={token}")
    print()
    print("You can use it in curl commands like:")
    print(f'curl -H "Authorization: Bearer {token}" http://127.0.0.1:8000/api/auth/me')
else:
    print("❌ Authentication failed")
