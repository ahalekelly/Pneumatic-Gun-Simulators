# Creating a Release

This document provides step-by-step instructions for creating a new release with pre-built executables.

## Overview

The release process is automated via GitHub Actions:
- **macOS**: Creates `.app` bundles using py-app-standalone wrapped in native macOS application structure
- **Windows**: Creates single `.exe` files using PyInstaller

## Step-by-Step Release Process

### 1. Ensure All Changes Are Committed

Make sure all your changes are committed to the main branch (or merge your feature branch):

```bash
git status  # Should show "nothing to commit, working tree clean"
```

### 2. Create a Version Tag

Create a git tag following semantic versioning (e.g., v0.1.0, v1.0.0):

```bash
# For the first release
git tag v0.1.0

# For subsequent releases
git tag v0.2.0  # Minor version bump
git tag v1.0.0  # Major version bump
```

### 3. Push the Tag to GitHub

```bash
git push origin v0.1.0  # Replace with your version number
```

**Important:** Use the exact tag you created. The tag must start with `v` to trigger the release workflow.

### 4. Monitor the Build Process

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. You should see a new workflow run called "Build Executables"
4. The workflow will:
   - Build macOS .app bundles
   - Build Windows .exe files
   - Create a GitHub release with downloadable artifacts

This process typically takes 5-10 minutes.

### 5. Verify the Release

Once the workflow completes:

1. Go to the "Releases" section of your GitHub repository
2. You should see a new release for your version tag
3. The release will contain two downloadable files:
   - `pneumatic-gun-simulators-macos.tar.gz` - Contains both .app bundles
   - `pneumatic-gun-simulators-windows.zip` - Contains both .exe files

### 6. Test the Executables (Recommended)

Download the artifacts and test them:

**macOS:**
```bash
# Download and extract
tar -xzf pneumatic-gun-simulators-macos.tar.gz

# Run the applications
open "Spring Plunger Simulator.app"
open "Nomad Simulator.app"
```

**Note for macOS users:** On first run, users may see a Gatekeeper warning:
```
"Apple could not verify [app] is free of malware..."
```

Users can bypass this by right-clicking the .app, selecting "Open", or running:
```bash
xattr -cr "Spring Plunger Simulator.app"
xattr -cr "Nomad Simulator.app"
```

**Windows:**
```powershell
# Extract the zip file
Expand-Archive pneumatic-gun-simulators-windows.zip

# Run the executables
.\nomad-simulator.exe
.\spring-plunger-simulator.exe
```

### 7. Add Release Notes (Optional)

You can edit the release on GitHub to add:
- Description of new features
- Bug fixes
- Known issues
- Installation instructions for end users

## Quick Reference Commands

```bash
# Create and push a new release
git tag v0.1.0
git push origin v0.1.0

# List existing tags
git tag -l

# Delete a tag if needed (use with caution)
git tag -d v0.1.0              # Delete locally
git push origin --delete v0.1.0  # Delete remotely
```

## Troubleshooting

### Build Fails

If the GitHub Actions build fails:
1. Check the Actions tab for error messages
2. Common issues:
   - Missing dependencies in pyproject.toml
   - Build script errors
   - GitHub Actions runner issues

### Tag Already Exists

If you accidentally created a tag:
```bash
# Delete local tag
git tag -d v0.1.0

# Delete remote tag (if already pushed)
git push origin --delete v0.1.0

# Create the correct tag
git tag v0.1.0
git push origin v0.1.0
```

## Manual Local Builds

You can also build executables locally for testing:

**macOS/Linux:**
```bash
./build.sh
# Output in dist/*.app (macOS) or py-standalone/ (Linux)
```

**Windows:**
```powershell
.\build.ps1
# Output in dist\*.exe
```

## Version Numbering Guide

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR** (v1.0.0, v2.0.0): Breaking changes or major new features
- **MINOR** (v0.1.0, v0.2.0): New features, backwards compatible
- **PATCH** (v0.1.1, v0.1.2): Bug fixes, backwards compatible

Examples:
- First release: `v0.1.0`
- Bug fix: `v0.1.1`
- New feature: `v0.2.0`
- Major rewrite: `v1.0.0`
