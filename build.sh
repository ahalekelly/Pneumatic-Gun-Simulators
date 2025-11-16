#!/bin/bash
# Build script for macOS and Linux executable builds using PyInstaller

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

# Install dependencies including PyInstaller
echo "Installing dependencies..."
uv sync --all-extras

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build executables
echo ""
echo "Building Nomad Simulator executable..."
uv run pyinstaller --onefile --windowed --name nomad-simulator src/nomad_ui.py

echo ""
echo "Building Spring Plunger Simulator executable..."
uv run pyinstaller --onefile --windowed --name spring-plunger-simulator src/dart_plunger_gui.py

echo ""
echo "Build complete!"
echo ""
echo "The standalone executables are located in:"
echo "  ./dist/"
echo ""
echo "Available executables:"
ls -lh dist/
