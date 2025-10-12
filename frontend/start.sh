#!/bin/bash

# Start frontend development server

echo "Starting AgenticCFO Frontend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Using .env.example defaults."
    echo "Consider copying .env.example to .env for custom configuration."
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "node_modules not found. Installing dependencies..."
    npm install
fi

# Start Vite development server
echo "Starting Vite development server on http://localhost:5173"
echo ""

npm run dev
