#!/bin/bash
# ConTiny Installation Script

set -e

echo "Installing ConTiny..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Install ConTiny
if [ -f "setup.py" ]; then
    echo "Installing from source..."
    pip3 install -e .
else
    echo "Installing from PyPI..."
    pip3 install continy
fi

# Create directories
mkdir -p ~/.continy/containers
mkdir -p ~/.continy/templates

# Verify installation
if command -v continy &> /dev/null; then
    echo "ConTiny installed successfully!"
    echo "Run 'continy --help' to get started."
else
    echo "Installation completed, but 'continy' command not found in PATH."
    echo "You may need to add ~/.local/bin to your PATH or restart your shell."
fi