#!/bin/bash
# ConTiny Uninstallation Script

set -e

echo "Uninstalling ConTiny..."

# Remove pip package
pip3 uninstall -y continy || echo "ConTiny package not found in pip"

# Remove user directories (with confirmation)
read -p "Remove ConTiny containers and data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf ~/.continy
    rm -rf ./containers
    echo "ConTiny data removed."
fi

echo "ConTiny uninstalled successfully!"