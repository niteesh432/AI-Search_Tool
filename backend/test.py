from database import SessionLocal
from sqlalchemy.sql import text  # Import text()

try:
    db = SessionLocal()
    db.execute(text("SELECT 1"))  # Wrap raw SQL in text()
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
finally:
    db.close()
