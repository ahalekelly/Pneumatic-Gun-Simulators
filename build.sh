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
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: Create .app bundles (no extraction needed, fast startup)
    echo "Building Nomad Simulator.app..."
    uv run pyinstaller --windowed --runtime-hook=hooks/runtime_hook_matplotlib.py \
        --osx-bundle-identifier com.pneumaticgunsimulators.nomad \
        --name "Nomad Simulator" src/nomad_ui.py

    echo ""
    echo "Building Spring Plunger Simulator.app..."
    uv run pyinstaller --windowed --runtime-hook=hooks/runtime_hook_matplotlib.py \
        --osx-bundle-identifier com.pneumaticgunsimulators.springplunger \
        --name "Spring Plunger Simulator" src/dart_plunger_gui.py
else
    # Linux: Create single executables
    echo "Building Nomad Simulator executable..."
    uv run pyinstaller --onefile --windowed --runtime-hook=hooks/runtime_hook_matplotlib.py --name nomad-simulator src/nomad_ui.py

    echo ""
    echo "Building Spring Plunger Simulator executable..."
    uv run pyinstaller --onefile --windowed --runtime-hook=hooks/runtime_hook_matplotlib.py --name spring-plunger-simulator src/dart_plunger_gui.py
fi

echo ""
echo "Build complete!"
echo ""
echo "The standalone executables are located in:"
echo "  ./dist/"
echo ""
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS .app bundles:"
    ls -d dist/*.app 2>/dev/null || echo "No .app bundles found"
else
    echo "Available executables:"
    ls -lh dist/
fi
