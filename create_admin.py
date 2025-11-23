import bcrypt
from app.database import supabase

# Admin credentials
email = "admin@terasinterior.com"
password = "Admin123!"  # GANTI INI dengan password yang aman!
name = "Admin Teras Interior"
role = "admin"

print("Creating admin user...")
print(f"Email: {email}")
print(f"Name: {name}")
print(f"Role: {role}")
print()

# Hash password using bcrypt directly
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
print("✓ Password hashed successfully")

# Insert to database
try:
    response = supabase.table('users').insert({
        'email': email,
        'password_hash': password_hash,
        'name': name,
        'role': role
    }).execute()
    
    print("✓ Admin user created successfully!")
    print()
    print("User Details:")
    print(f"  ID: {response.data[0]['id']}")
    print(f"  Email: {response.data[0]['email']}")
    print(f"  Name: {response.data[0]['name']}")
    print(f"  Role: {response.data[0]['role']}")
    print()
    print("⚠️  IMPORTANT: Save these credentials securely!")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    
except Exception as e:
    print(f"✗ Error creating admin user: {e}")
    print()
    print("Possible reasons:")
    print("  - User with this email already exists")
    print("  - Database connection error")
    print("  - Check your .env file configuration")
