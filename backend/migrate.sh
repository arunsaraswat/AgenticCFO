#!/bin/bash

# Database migration script

echo "AgenticCFO Database Migration Tool"
echo "===================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your database settings."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check command
case "$1" in
    "upgrade")
        echo "Running database migrations..."
        alembic upgrade head
        echo "Migration complete!"
        ;;
    "downgrade")
        echo "Rolling back last migration..."
        alembic downgrade -1
        echo "Rollback complete!"
        ;;
    "create")
        if [ -z "$2" ]; then
            echo "Error: Migration message required"
            echo "Usage: ./migrate.sh create 'migration message'"
            exit 1
        fi
        echo "Creating new migration: $2"
        alembic revision --autogenerate -m "$2"
        echo "Migration file created!"
        ;;
    "history")
        echo "Migration history:"
        alembic history
        ;;
    "current")
        echo "Current migration:"
        alembic current
        ;;
    *)
        echo "Usage: ./migrate.sh {upgrade|downgrade|create|history|current}"
        echo ""
        echo "Commands:"
        echo "  upgrade    - Apply all pending migrations"
        echo "  downgrade  - Rollback the last migration"
        echo "  create     - Create a new migration (requires message)"
        echo "  history    - Show migration history"
        echo "  current    - Show current migration"
        echo ""
        echo "Examples:"
        echo "  ./migrate.sh upgrade"
        echo "  ./migrate.sh create 'add users table'"
        exit 1
        ;;
esac
