"""Fix admin password"""
import bcrypt
from sqlalchemy import create_engine, text
from app.config import settings

# Generate new password hash
password = "admin123"
new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(f"New password hash: {new_hash.decode('utf-8')}")

# Update database
engine = create_engine(settings.database_url)
with engine.begin() as conn:  # Use begin() for auto-commit
    conn.execute(
        text("UPDATE users SET password_hash = :hash WHERE email = 'admin@terasinterior.com'"),
        {"hash": new_hash.decode('utf-8')}
    )
    print("✅ Password updated successfully!")

# Verify
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT password_hash FROM users WHERE email = 'admin@terasinterior.com'")
    )
    user = result.fetchone()
    
    # Test password
    is_valid = bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
    if is_valid:
        print("✅ Password verification SUCCESS!")
    else:
        print("❌ Password verification FAILED!")
