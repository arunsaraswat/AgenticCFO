"""Test database connection script."""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

def test_connection():
    """Test database connection."""
    print(f"Testing connection to database...")
    print(f"Database URL: {settings.database_url[:30]}...{settings.database_url[-20:]}")

    try:
        # Create engine
        engine = create_engine(settings.database_url)

        # Try to connect
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"\n✓ Connection successful!")
            print(f"PostgreSQL version: {version}")
            return True

    except Exception as e:
        print(f"\n✗ Connection failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
