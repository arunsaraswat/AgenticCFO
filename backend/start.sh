#!/bin/bash

# Start backend server script

echo "Starting AgenticCFO Backend Server..."

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

# Start uvicorn server
echo "Starting Uvicorn server on http://localhost:8000"
echo "API Documentation available at http://localhost:8000/docs"
echo "ReDoc documentation available at http://localhost:8000/redoc"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
