# Build script for Windows executable builds using PyInstaller

$ErrorActionPreference = "Stop"

Write-Host "Building standalone executables for Pneumatic Gun Simulators..." -ForegroundColor Green
Write-Host "Platform: Windows"
Write-Host ""

# Check if uv is installed
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: uv is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "  powershell -ExecutionPolicy ByPass -c `"irm https://astral.sh/uv/install.ps1 | iex`""
    exit 1
}

$uvVersion = uv --version
Write-Host "Using uv version: $uvVersion"
Write-Host ""

# Install dependencies including PyInstaller
Write-Host "Installing dependencies..."
uv sync --all-extras

# Convert PNG icons to .ico format
Write-Host ""
Write-Host "Converting icons to .ico format..."
uv run python convert_icons.py

# Clean previous builds
Write-Host "Cleaning previous builds..."
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path dist) { Remove-Item -Recurse -Force dist }

# Build executables
Write-Host ""
Write-Host "Building Nomad Simulator executable..."
uv run pyinstaller --onefile --windowed --name nomad-simulator --icon icons/nomad-icon.ico src/nomad_ui.py

Write-Host ""
Write-Host "Building Spring Plunger Simulator executable..."
uv run pyinstaller --onefile --windowed --name spring-plunger-simulator --icon icons/spring-plunger-icon.ico src/dart_plunger_gui.py

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "The standalone executables are located in:"
Write-Host "  .\dist\"
Write-Host ""
Write-Host "Available executables:"
Get-ChildItem dist\*.exe | Format-Table Name, Length -AutoSize

