#!/bin/bash
# Build script for macOS and Linux executable builds using py-app-standalone

set -e  # Exit on error

echo "Building standalone executables for Pneumatic Gun Simulators..."
echo "Platform: $(uname -s)"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "Using uv version: $(uv --version)"
echo ""

# Update uv to ensure we have the latest version
echo "Updating uv..."
uv self update || echo "Warning: Could not update uv, continuing with current version"
echo ""

# Build the standalone distribution
echo "Building standalone Python environment with pneumatic-gun-simulators..."
uvx py-app-standalone pneumatic-gun-simulators

echo ""
echo "Build complete!"
echo ""
echo "The standalone executables are located in:"
echo "  ./py-standalone/cpython-*/bin/"
echo ""
echo "Available executables:"
echo "  - nomad-simulator"
echo "  - spring-plunger-simulator"
echo ""
echo "You can move the entire py-standalone directory to any compatible system."
