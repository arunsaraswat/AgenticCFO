#!/bin/bash

# Run frontend tests with coverage

echo "Running AgenticCFO Frontend Tests"
echo "=================================="

# Check for specific test arguments
if [ -n "$1" ]; then
    echo "Running specific tests: $@"
    npm test -- "$@"
else
    echo "Running all tests with coverage..."
    npm run test:coverage
fi

# Show test results
if [ $? -eq 0 ]; then
    echo ""
    echo "Tests completed successfully!"
    echo "Coverage report available at: coverage/lcov-report/index.html"
fi
