# Build script for Windows executable builds using py-app-standalone

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

# Clean previous builds
Write-Host "Cleaning previous builds..."
if (Test-Path py-standalone) { Remove-Item -Recurse -Force py-standalone }

# Build the standalone distribution from local package (source-only to avoid .pyc path issues)
Write-Host "Building standalone Python environment from local package..."
uvx py-app-standalone . --source-only

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "The standalone executables are located in:"
Write-Host "  .\py-standalone\cpython-*\Scripts\"
Write-Host ""
Write-Host "Available executables:"
Get-ChildItem -Recurse py-standalone -Include nomad-simulator.exe,spring-plunger-simulator.exe | Select-Object FullName
Write-Host ""
Write-Host "You can move the entire py-standalone directory to any compatible Windows system."

