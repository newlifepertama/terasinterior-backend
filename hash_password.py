#!/usr/bin/env python3
"""
Hash password dengan bcrypt untuk update database
"""

import bcrypt
import sys

def hash_password(password: str) -> str:
    """Hash password dengan bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password dengan hash"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hash_password.py <password>")
        sys.exit(1)
    
    password = sys.argv[1]
    hashed = hash_password(password)
    
    print("=" * 60)
    print("BCRYPT PASSWORD HASH")
    print("=" * 60)
    print(f"Password: {password}")
    print(f"Hash: {hashed}")
    print("=" * 60)
    print("\nSQL UPDATE:")
    print("=" * 60)
    print(f"""
UPDATE users 
SET password = '{hashed}'
WHERE email = 'admin@terasinterior.com';
""")
    print("=" * 60)
    
    # Verify
    is_valid = verify_password(password, hashed)
    print(f"\nVerification: {'✅ VALID' if is_valid else '❌ INVALID'}")
    print("=" * 60)
