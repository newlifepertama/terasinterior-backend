"""Test database connection"""
from sqlalchemy import create_engine, text
from app.config import settings

def test_connection():
    try:
        # Create engine
        engine = create_engine(settings.database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print("✅ Database connection successful!")
            print(f"PostgreSQL version: {version}")
            
            # Test users table
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.fetchone()[0]
            print(f"✅ Users table exists with {count} users")
            
            # Get admin user
            result = conn.execute(text("SELECT email, name, role FROM users WHERE email = 'admin@terasinterior.com'"))
            user = result.fetchone()
            if user:
                print(f"✅ Admin user found: {user.email} ({user.name}) - Role: {user.role}")
            else:
                print("❌ Admin user not found!")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()
