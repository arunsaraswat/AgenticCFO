"""Seed database with test data."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def seed_database():
    """
    Seed database with initial test data.

    Creates sample users for development and testing.
    """
    db: Session = SessionLocal()

    try:
        print("Starting database seeding...")

        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already contains {existing_users} users. Skipping seed.")
            return

        # Create admin user
        admin_user = User(
            email="admin@agenticcfo.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123456"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)

        # Create regular test users
        test_users = [
            {
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "password": "johndoe123"
            },
            {
                "email": "jane.smith@example.com",
                "full_name": "Jane Smith",
                "password": "janesmith123"
            },
            {
                "email": "bob.wilson@example.com",
                "full_name": "Bob Wilson",
                "password": "bobwilson123"
            }
        ]

        for user_data in test_users:
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                is_active=True,
                is_superuser=False
            )
            db.add(user)

        db.commit()

        print("Database seeded successfully!")
        print("\nCreated users:")
        print("  - admin@agenticcfo.com (Admin) - Password: admin123456")
        print("  - john.doe@example.com - Password: johndoe123")
        print("  - jane.smith@example.com - Password: janesmith123")
        print("  - bob.wilson@example.com - Password: bobwilson123")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
