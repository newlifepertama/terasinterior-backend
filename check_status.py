"""Check current system status"""
from app.database import get_db
from sqlalchemy import text

db = next(get_db())

print("=" * 50)
print("DATABASE STATUS CHECK")
print("=" * 50)

tables = ['users', 'portfolio', 'services', 'contacts', 'settings']

for table in tables:
    try:
        result = db.execute(text(f'SELECT COUNT(*) FROM {table}'))
        count = result.scalar()
        print(f"✅ {table.upper()}: {count} records")
    except Exception as e:
        print(f"❌ {table.upper()}: Error - {e}")

print("=" * 50)
