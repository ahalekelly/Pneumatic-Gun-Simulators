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

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf py-standalone

# Build the standalone distribution from local package
echo "Building standalone Python environment from local package..."
uvx py-app-standalone . --source-only

echo ""
echo "Build complete!"
echo ""
echo "The standalone executables are located in:"
echo "  ./py-standalone/cpython-*/bin/"
echo ""
echo "Available executables:"
find py-standalone -name "nomad-simulator" -o -name "spring-plunger-simulator"
echo ""
echo "You can move the entire py-standalone directory to any compatible system."

