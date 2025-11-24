#!/usr/bin/env python3
import sys
import bcrypt
from sqlalchemy import text
from app.database import SessionLocal

# Admin credentials
username = "admin"
email = "admin@terasinterior.com"
password = "Admin123!"  # GANTI INI dengan password yang aman!

print("=" * 50)
print("CREATE ADMIN USER - TERAS INTERIOR")
print("=" * 50)
print(f"Username: {username}")
print(f"Email: {email}")
print(f"Password: {password}")
print()
print("⚠️  PENTING: Ganti password setelah login pertama!")
print()

# Hash password using bcrypt
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
print("✓ Password berhasil di-hash")

# Insert to database
db = SessionLocal()
try:
    # Check if user already exists
    result = db.execute(
        text("SELECT id, username, email FROM admin_users WHERE email = :email OR username = :username"),
        {"email": email, "username": username}
    )
    existing_user = result.fetchone()
    
    if existing_user:
        print()
        print("⚠️  User sudah ada!")
        print(f"   ID: {existing_user[0]}")
        print(f"   Username: {existing_user[1]}")
        print(f"   Email: {existing_user[2]}")
        print()
        print("Untuk reset password, gunakan script reset_admin_password.py")
        db.close()
        sys.exit(0)
    
    # Insert admin user
    result = db.execute(
        text("""
            INSERT INTO admin_users (username, email, hashed_password, is_active)
            VALUES (:username, :email, :hashed_password, true)
            RETURNING id, username, email, created_at
        """),
        {
            "username": username,
            "email": email,
            "hashed_password": hashed_password
        }
    )
    db.commit()
    
    user = result.fetchone()
    
    print()
    print("=" * 50)
    print("✓ ADMIN USER BERHASIL DIBUAT!")
    print("=" * 50)
    print(f"ID: {user[0]}")
    print(f"Username: {user[1]}")
    print(f"Email: {user[2]}")
    print(f"Created: {user[3]}")
    print()
    print("CREDENTIALS:")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print()
    print("⚠️  Simpan credentials ini dengan aman!")
    print("⚠️  Ganti password setelah login pertama!")
    print()
    
except Exception as e:
    db.rollback()
    print()
    print(f"✗ ERROR: {e}")
    print()
    print("Possible reasons:")
    print("  - Database connection error")
    print("  - Check your .env file configuration")
    sys.exit(1)
finally:
    db.close()
