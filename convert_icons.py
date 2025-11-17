#!/usr/bin/env python3
"""Convert PNG icons to .ico format for Windows executables."""

from PIL import Image
import sys

def png_to_ico(png_path, ico_path, sizes=None):
    """Convert PNG to ICO with multiple sizes."""
    if sizes is None:
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

    img = Image.open(png_path)

    # Create list of images at different sizes
    icon_sizes = []
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        icon_sizes.append(resized)

    # Save as ICO
    icon_sizes[0].save(ico_path, format='ICO', sizes=[s for s in sizes])
    print(f"Created {ico_path}")

if __name__ == "__main__":
    # Convert both icons
    png_to_ico("icons/spring-piston-icon.png", "icons/spring-piston-icon.ico")
    png_to_ico("icons/nomad-icon.png", "icons/nomad-icon.ico")
    print("Icon conversion complete!")
