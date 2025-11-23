from app.database import supabase

print("Checking existing admin users...")
print()

try:
    response = supabase.table('users').select('*').eq('role', 'admin').execute()
    
    if response.data:
        print(f"✓ Found {len(response.data)} admin user(s):")
        print()
        for user in response.data:
            print(f"  ID: {user['id']}")
            print(f"  Email: {user['email']}")
            print(f"  Name: {user['name']}")
            print(f"  Role: {user['role']}")
            print(f"  Created: {user.get('created_at', 'N/A')}")
            print()
    else:
        print("✗ No admin users found")
        
except Exception as e:
    print(f"✗ Error: {e}")
