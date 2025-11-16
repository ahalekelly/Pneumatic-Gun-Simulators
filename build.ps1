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

# Update uv to ensure we have the latest version
Write-Host "Updating uv..."
try {
    uv self update
} catch {
    Write-Host "Warning: Could not update uv, continuing with current version" -ForegroundColor Yellow
}
Write-Host ""

# Build the standalone distribution
Write-Host "Building standalone Python environment with pneumatic-gun-simulators..."
uvx py-app-standalone pneumatic-gun-simulators

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "The standalone executables are located in:"
Write-Host "  .\py-standalone\cpython-*\Scripts\"
Write-Host ""
Write-Host "Available executables:"
Write-Host "  - nomad-simulator.exe"
Write-Host "  - spring-plunger-simulator.exe"
Write-Host ""
Write-Host "You can move the entire py-standalone directory to any compatible Windows system."
