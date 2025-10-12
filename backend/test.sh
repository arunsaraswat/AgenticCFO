#!/bin/bash

# Run backend tests with coverage

echo "Running AgenticCFO Backend Tests"
echo "================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check for specific test arguments
if [ -n "$1" ]; then
    echo "Running specific tests: $@"
    pytest "$@"
else
    echo "Running all tests with coverage..."
    pytest
fi

# Show coverage report location
if [ $? -eq 0 ]; then
    echo ""
    echo "Tests completed successfully!"
    echo "HTML coverage report available at: htmlcov/index.html"
fi
