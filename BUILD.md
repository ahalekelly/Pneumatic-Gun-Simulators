# Building Standalone Executables

This project uses [py-app-standalone](https://github.com/jlevy/py-app-standalone) to create self-contained, relocatable executables for macOS and Windows.

## Prerequisites

You need to have `uv` installed on your system:

### macOS and Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Building Locally

**Important:** You must build on the same platform you want to run on:
- Build macOS executables on a Mac
- Build Windows executables on Windows

### macOS / Linux

```bash
./build.sh
```

### Windows

```powershell
.\build.ps1
```

## Build Output

After building, you'll find the executables in:

- **macOS/Linux:** `./py-standalone/cpython-*/bin/`
  - `nomad-simulator`
  - `spring-plunger-simulator`

- **Windows:** `.\py-standalone\cpython-*\Scripts\`
  - `nomad-simulator.exe`
  - `spring-plunger-simulator.exe`

The entire `py-standalone` directory is relocatable and can be moved to any compatible system without requiring Python or any dependencies to be installed.

## GitHub Actions

The project includes automated builds via GitHub Actions:

1. **Automatic builds** run on every push to `main` and on pull requests
2. **Tagged releases** (e.g., `v1.0.0`) automatically create GitHub releases with downloadable executables

To create a release:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

The workflow will automatically build both macOS and Windows executables and attach them to the GitHub release.

## Manual Workflow Trigger

You can also manually trigger the build workflow from the GitHub Actions tab in your repository.

## What's Included

The standalone distribution includes:
- Python interpreter (version 3.13)
- All dependencies (scipy, matplotlib, numpy, etc.)
- Both GUI applications:
  - **Nomad Simulator**: Precompressed air gun simulator
  - **Spring Plunger Simulator**: Spring piston gun simulator

## Troubleshooting

### uv not found
Make sure `uv` is in your PATH. After installation, you may need to restart your terminal or add it to your PATH manually.

### Build fails
1. Update uv to the latest version: `uv self update`
2. Check that you have an internet connection (needed to download dependencies)
3. On macOS, ensure you have Xcode command line tools installed: `xcode-select --install`

### Executables don't run
- Ensure you're running on a compatible system (same OS and architecture as the build)
- On macOS, you may need to grant permission in System Preferences > Security & Privacy
- The entire `py-standalone` directory must be kept together (don't try to move just the executable)

## Advanced Usage

You can also build manually using `uvx`:

```bash
uvx py-app-standalone pneumatic-gun-simulators
```

This gives you more control over the build process and allows you to customize options.
