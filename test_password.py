"""Test password verification"""
import bcrypt
from sqlalchemy import create_engine, text
from app.config import settings

def test_password():
    try:
        # Create engine
        engine = create_engine(settings.database_url)
        
        # Get user from database
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT email, password_hash FROM users WHERE email = 'admin@terasinterior.com'")
            )
            user = result.fetchone()
            
            if not user:
                print("❌ User not found!")
                return
            
            print(f"✅ User found: {user.email}")
            print(f"Password hash in DB: {user.password_hash[:50]}...")
            
            # Test password
            test_password = "admin123"
            print(f"\nTesting password: {test_password}")
            
            try:
                is_valid = bcrypt.checkpw(
                    test_password.encode('utf-8'),
                    user.password_hash.encode('utf-8')
                )
                
                if is_valid:
                    print("✅ Password verification SUCCESS!")
                else:
                    print("❌ Password verification FAILED!")
                    
            except Exception as e:
                print(f"❌ Password check error: {e}")
                
                # Generate new hash
                print("\n🔧 Generating new password hash...")
                new_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
                print(f"New hash: {new_hash.decode('utf-8')}")
                
                # Update database
                conn.execute(
                    text("UPDATE users SET password_hash = :hash WHERE email = 'admin@terasinterior.com'"),
                    {"hash": new_hash.decode('utf-8')}
                )
                conn.commit()
                print("✅ Password hash updated in database!")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_password()
