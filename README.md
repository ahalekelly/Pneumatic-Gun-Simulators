# Pneumatic-Gun-Simulators

This repository contains calculators for pneumatic spring-piston and precompressed air guns. Both calculators run off a TKinter GUI.
Equations will be posted later, but they are all 1-D lumped parameter simulations. Simple flow physics will be added in the future.

## Applications

- **Nomad Simulator** (`nomad_ui.py`): Precompressed air gun simulator
- **Spring Piston Simulator** (`dart_plunger_gui.py`): Spring piston gun simulator

## Running from Source

### Installation
[Install the uv package manager](https://docs.astral.sh/uv/getting-started/installation/)

### Running the applications
In the terminal run:
```bash
# For the Nomad (precompressed air) simulator
uv run src/nomad_ui.py

# For the Spring Piston simulator
uv run src/dart_plunger_gui.py
```

Alternatively, you can use the installed scripts:
```bash
uv run nomad-simulator
uv run spring-piston-simulator
```

## Building Standalone Executables

This project supports building standalone executables for macOS and Windows that don't require Python or any dependencies to be installed.

See [BUILD.md](BUILD.md) for detailed instructions on:
- Building executables locally
- Automated builds via GitHub Actions
- Creating releases with pre-built executables

### Quick Start

**macOS/Linux:**
```bash
./build.sh
```

**Windows:**
```powershell
.\build.ps1
```

The executables will be in the `py-standalone/` directory:
- **macOS/Linux**: `py-standalone/cpython-*/bin/nomad-simulator` and `spring-piston-simulator`
- **Windows**: `py-standalone\cpython-*\Scripts\nomad-simulator.exe` and `spring-piston-simulator.exe`

The entire `py-standalone` directory is relocatable and can be moved anywhere.