#!/bin/bash

# AgenticCFO - Full Stack Application Launcher
# This script starts both backend and frontend servers

set -e  # Exit on error

echo "================================================"
echo "  AgenticCFO - Full Stack Application Launcher"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if backend .env exists
if [ ! -f backend/.env ]; then
    echo -e "${RED}Error: backend/.env file not found!${NC}"
    echo "Please copy backend/.env.example to backend/.env and configure your settings."
    echo ""
    echo "Steps:"
    echo "  1. cd backend"
    echo "  2. cp .env.example .env"
    echo "  3. Edit .env with your Supabase credentials"
    exit 1
fi

# Check if frontend .env exists (optional, has defaults)
if [ ! -f frontend/.env ]; then
    echo -e "${YELLOW}Warning: frontend/.env not found. Using defaults from .env.example${NC}"
fi

echo -e "${BLUE}Checking backend dependencies...${NC}"
# Check if backend virtual environment exists
if [ ! -d backend/venv ] && [ ! -d backend/.venv ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo -e "${GREEN}Backend dependencies installed!${NC}"
else
    echo -e "${GREEN}Backend virtual environment found.${NC}"
fi

echo ""
echo -e "${BLUE}Checking frontend dependencies...${NC}"
# Check if frontend node_modules exists
if [ ! -d frontend/node_modules ]; then
    echo -e "${YELLOW}node_modules not found. Installing...${NC}"
    cd frontend
    npm install
    cd ..
    echo -e "${GREEN}Frontend dependencies installed!${NC}"
else
    echo -e "${GREEN}Frontend dependencies found.${NC}"
fi

echo ""
echo -e "${BLUE}Running database migrations...${NC}"
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

alembic upgrade head
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Database migrations completed!${NC}"
else
    echo -e "${RED}Migration failed. Please check your database configuration.${NC}"
    exit 1
fi
cd ..

echo ""
echo -e "${GREEN}Starting servers...${NC}"
echo ""
echo "Backend will start on:  http://localhost:8000"
echo "Frontend will start on: http://localhost:5173"
echo ""
echo "API Documentation:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc:      http://localhost:8000/redoc"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""
echo "================================================"
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping servers...${NC}"
    kill $(jobs -p) 2>/dev/null
    echo -e "${GREEN}All servers stopped. Goodbye!${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend in background
echo -e "${BLUE}[Backend]${NC} Starting..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 2>&1 | sed "s/^/[Backend]  /" &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo -e "${BLUE}[Frontend]${NC} Starting..."
cd frontend
npm run dev 2>&1 | sed "s/^/[Frontend] /" &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait
