# Pneumatic-Gun-Simulators

This repository contains calculators for pneumatic spring-piston and precompressed air guns. Both calculators run off a TKinter GUI.
Equations will be posted later, but they are all 1-D lumped parameter simulations. Simple flow physics will be added in the future.

## Applications

- **Spring Piston Simulator** (`spring_piston_gui.py`): Spring piston gun simulator
- **Nomad Simulator** (`nomad_ui.py`): Precompressed air gun simulator

## Usage

You can download compiled applications for Windows and MacOS from the Releases tab on the right

## Running from Source

[Install the uv package manager](https://docs.astral.sh/uv/getting-started/installation/)

In the terminal run:
```bash
# For the Spring Piston simulator
uv run src/spring_piston_gui.py

# For the Nomad (precompressed air) simulator
uv run src/nomad_ui.py
```