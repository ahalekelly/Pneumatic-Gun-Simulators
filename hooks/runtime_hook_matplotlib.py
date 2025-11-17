"""
PyInstaller runtime hook for matplotlib to fix font cache performance on macOS.

This sets MPLCONFIGDIR to a persistent location and configures matplotlib
to skip the expensive font discovery process on every launch.

Reference: https://github.com/matplotlib/matplotlib/issues/13071
"""
import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    # Set matplotlib config directory to a persistent location
    app_name = 'PneumaticGunSimulators'

    # Use platform-appropriate config directory
    if sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/PneumaticGunSimulators
        config_dir = Path.home() / 'Library' / 'Application Support' / app_name
    elif sys.platform == 'win32':
        # Windows: %LOCALAPPDATA%\PneumaticGunSimulators
        config_dir = Path(os.environ.get('LOCALAPPDATA', Path.home())) / app_name
    else:
        # Linux: ~/.config/PneumaticGunSimulators
        config_dir = Path.home() / '.config' / app_name

    # Create directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)

    # Set the matplotlib config directory
    os.environ['MPLCONFIGDIR'] = str(config_dir)

    # Disable font manager's font discovery to speed up startup
    # This makes matplotlib use only built-in fonts
    os.environ['MPLBACKEND'] = 'TkAgg'

    # Set matplotlib to use a minimal font set
    import matplotlib
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']

