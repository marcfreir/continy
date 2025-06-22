#!/bin/bash
# ConTiny Build Script

set -e

echo "Building ConTiny..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Run tests
if [ -d "tests" ]; then
    echo "Running tests..."
    python3 -m pytest tests/ -v
fi

# Build package
echo "Building package..."
python3 setup.py sdist bdist_wheel

# Check package
echo "Checking package..."
python3 -m twine check dist/*

echo "Build completed successfully!"
echo "Distribution files created in dist/"