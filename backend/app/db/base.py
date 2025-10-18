"""Database base configuration."""
from sqlalchemy.ext.declarative import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()

# Note: Models are imported in alembic/env.py for migrations
# We don't import them here to avoid circular import issues
