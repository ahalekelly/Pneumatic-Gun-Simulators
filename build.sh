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

# On macOS, create .app bundles
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "Creating macOS .app bundles..."

    # Find the Python installation directory
    PYTHON_DIR=$(find py-standalone -maxdepth 1 -name "cpython-*" -type d | head -1)

    if [ -z "$PYTHON_DIR" ]; then
        echo "Error: Could not find Python installation directory"
        exit 1
    fi

    # Function to create .app bundle
    create_app_bundle() {
        local APP_NAME="$1"
        local EXECUTABLE_NAME="$2"
        local BUNDLE_ID="$3"

        echo "Creating $APP_NAME.app..."

        # Create .app structure
        mkdir -p "dist/$APP_NAME.app/Contents/MacOS"
        mkdir -p "dist/$APP_NAME.app/Contents/Resources"

        # Copy the entire py-standalone directory into Resources
        cp -R py-standalone "dist/$APP_NAME.app/Contents/Resources/"

        # Create launcher script
        cat > "dist/$APP_NAME.app/Contents/MacOS/$APP_NAME" << 'EOF'
#!/bin/bash
# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Run the actual Python executable
exec "$DIR/../Resources/py-standalone/cpython-"*"/bin/EXEC_NAME" "$@"
EOF
        # Replace EXEC_NAME with actual executable name
        sed -i '' "s/EXEC_NAME/$EXECUTABLE_NAME/g" "dist/$APP_NAME.app/Contents/MacOS/$APP_NAME"
        chmod +x "dist/$APP_NAME.app/Contents/MacOS/$APP_NAME"

        # Create Info.plist
        cat > "dist/$APP_NAME.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>
    <string>$BUNDLE_ID</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>0.1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
    }

    # Create dist directory
    mkdir -p dist

    # Create both .app bundles
    create_app_bundle "Spring Plunger Simulator" "spring-plunger-simulator" "com.pneumaticgunsimulators.springplunger"
    create_app_bundle "Nomad Simulator" "nomad-simulator" "com.pneumaticgunsimulators.nomad"

    echo ""
    echo "macOS .app bundles created in dist/"
fi

echo ""
echo "Build complete!"
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS .app bundles are located in:"
    echo "  ./dist/"
    echo ""
    echo "Available applications:"
    ls -d dist/*.app
    echo ""
    echo "Double-click the .app files to launch, or run:"
    echo "  open 'dist/Spring Plunger Simulator.app'"
    echo "  open 'dist/Nomad Simulator.app'"
else
    echo "The standalone executables are located in:"
    echo "  ./py-standalone/cpython-*/bin/"
    echo ""
    echo "Available executables:"
    find py-standalone -name "nomad-simulator" -o -name "spring-plunger-simulator"
    echo ""
    echo "You can move the entire py-standalone directory to any compatible system."
fi

