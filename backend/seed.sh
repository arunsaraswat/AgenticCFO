#!/bin/bash

# Seed database with test data

echo "Seeding AgenticCFO Database..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your settings."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run seed script
python scripts/seed.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Database seeded successfully!"
else
    echo ""
    echo "Error seeding database. Please check the error messages above."
    exit 1
fi
