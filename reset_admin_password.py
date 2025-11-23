import bcrypt
from app.database import supabase

# New admin password
new_password = "admin123"  # Simple password for testing

print("Resetting admin password...")
print(f"New password: {new_password}")
print()

# Hash password using bcrypt
password_bytes = new_password.encode('utf-8')
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

print(f"✓ Password hashed: {password_hash[:50]}...")
print()

# Update admin user password
try:
    response = supabase.table('users').update({
        'password_hash': password_hash
    }).eq('email', 'admin@terasinterior.com').execute()
    
    if response.data:
        print("✓ Admin password updated successfully!")
        print()
        print("Login credentials:")
        print(f"  Email: admin@terasinterior.com")
        print(f"  Password: {new_password}")
        print()
        print("⚠️  Save these credentials!")
    else:
        print("✗ Failed to update password")
        
except Exception as e:
    print(f"✗ Error: {e}")
