# Building Standalone Executables

This project uses [PyInstaller](https://pyinstaller.org/) to create standalone executables for macOS and Windows.

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

After building, you'll find the executables in the `dist/` directory:

- **macOS/Linux:** `./dist/`
  - `nomad-simulator`
  - `spring-plunger-simulator`

- **Windows:** `.\dist\`
  - `nomad-simulator.exe`
  - `spring-plunger-simulator.exe`

Each executable is a single file that bundles Python and all dependencies. You can copy and run them on any compatible system without requiring Python or dependencies to be installed.

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

Each executable includes:
- Python interpreter
- All dependencies (scipy, matplotlib, numpy, etc.)
- Application code

Available applications:
- **nomad-simulator**: Precompressed air gun simulator
- **spring-plunger-simulator**: Spring piston gun simulator

## Troubleshooting

### uv not found
Make sure `uv` is in your PATH. After installation, you may need to restart your terminal.

### Build fails
1. Make sure you have an internet connection (needed to download dependencies)
2. On macOS, ensure you have Xcode command line tools installed: `xcode-select --install`
3. On Windows, you may need to allow the script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Executables don't run
- Ensure you're running on a compatible system (same OS as the build)
- On macOS, you may need to grant permission in System Preferences > Security & Privacy:
  - Right-click the app and select "Open" the first time you run it
  - Or run: `xattr -cr dist/nomad-simulator` to remove quarantine attributes
- On Windows, you may need to allow the app through Windows Defender

### PyInstaller-specific issues

If you encounter issues with the build:
- Delete the `build/` and `dist/` directories and try again
- Check the PyInstaller warnings during build - some missing modules may need to be explicitly included

## Advanced Usage

### Custom PyInstaller Options

You can customize the build by editing the PyInstaller commands in `build.sh` or `build.ps1`:

- `--onefile`: Creates a single executable file (current default)
- `--windowed`: Prevents console window from appearing (current default)
- `--icon=icon.ico`: Add a custom icon
- `--add-data`: Include additional data files
- `--hidden-import`: Explicitly import modules that PyInstaller misses

Example:
```bash
uv run pyinstaller --onefile --windowed --icon=icon.ico --name nomad-simulator src/nomad_ui.py
```

### Building without uv

If you prefer not to use uv, you can build with regular Python:

```bash
pip install -e ".[build]"
pyinstaller --onefile --windowed --name nomad-simulator src/nomad_ui.py
pyinstaller --onefile --windowed --name spring-plunger-simulator src/dart_plunger_gui.py
```

## Size Optimization

The executables are quite large (~100MB+) because they include the entire Python runtime and scientific libraries. This is normal for PyInstaller builds with matplotlib and scipy.

To reduce size:
- Consider using `--onedir` instead of `--onefile` (creates a folder instead of a single file)
- Use UPX compression: `--upx-dir=/path/to/upx` (may cause antivirus false positives)
