#!/bin/bash

APP_NAME="Reconal"
ICON_PNG="Reconal_icon.png"
ICON_ICNS="Reconal.icns"
OUTPUT_DMG="Reconal_Installer.dmg"

echo "[*] Starting Build Process for $APP_NAME..."

# 1. Dependency Check
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 is not installed."
    exit 1
fi

echo "[*] Installing Dependencies..."
pip3 install -r requirements_desktop.txt

# 2. Icon Conversion (PNG -> ICNS)
# macOS apps strictly require .icns. PyInstaller will error or ignore PNG.
echo "[*] Converting Icon to .icns..."
if [ -f "$ICON_PNG" ]; then
    # Create a temporary iconset directory
    mkdir -p "$APP_NAME.iconset"
    
    # Generate various sizes (Required for a valid iconset/icns usually)
    sips -z 16 16     "$ICON_PNG" --out "$APP_NAME.iconset/icon_16x16.png" > /dev/null
    sips -z 32 32     "$ICON_PNG" --out "$APP_NAME.iconset/icon_16x16@2x.png" > /dev/null
    sips -z 32 32     "$ICON_PNG" --out "$APP_NAME.iconset/icon_32x32.png" > /dev/null
    sips -z 64 64     "$ICON_PNG" --out "$APP_NAME.iconset/icon_32x32@2x.png" > /dev/null
    sips -z 128 128   "$ICON_PNG" --out "$APP_NAME.iconset/icon_128x128.png" > /dev/null
    sips -z 256 256   "$ICON_PNG" --out "$APP_NAME.iconset/icon_128x128@2x.png" > /dev/null
    sips -z 256 256   "$ICON_PNG" --out "$APP_NAME.iconset/icon_256x256.png" > /dev/null
    sips -z 512 512   "$ICON_PNG" --out "$APP_NAME.iconset/icon_256x256@2x.png" > /dev/null
    sips -z 512 512   "$ICON_PNG" --out "$APP_NAME.iconset/icon_512x512.png" > /dev/null
    # If source is big enough
    sips -z 1024 1024 "$ICON_PNG" --out "$APP_NAME.iconset/icon_512x512@2x.png" > /dev/null

    # Convert iconset to icns
    iconutil -c icns "$APP_NAME.iconset"
    
    # Cleanup
    rm -rf "$APP_NAME.iconset"
    echo "    Icon converted successfully."
else
    echo "[!] $ICON_PNG not found. Proceeding without custom icon."
fi

# 3. Clean previous builds
echo "[*] Cleaning previous builds..."
rm -rf build dist "$OUTPUT_DMG"

# 4. PyInstaller Bundle
echo "[*] Running PyInstaller..."
# --windowed: No terminal window
# --noconsole: Same (Standard for macOS .app)
# --add-data: Include static folder
# --icon: Set app icon
# --name: App name
# --onefile: Not recommended for .app bundles usually, but we want a folder for .app structure. 
# PyInstaller default for macOS is a directory which constitutes the .app bundle contents.
pyinstaller --noconsole \
            --windowed \
            --name "$APP_NAME" \
            --icon "$ICON_ICNS" \
            --add-data "static:static" \
            reconal_app.py

if [ ! -d "dist/$APP_NAME.app" ]; then
    echo "[!] PyInstaller failed to create .app bundle."
    exit 1
fi

echo "[*] .app Bundle created at dist/$APP_NAME.app"

# 5. Create DMG (Distribution)
echo "[*] Creating DMG Installer..."
DMG_STAGING="dist/dmg_staging"
mkdir -p "$DMG_STAGING"

# Copy App
cp -r "dist/$APP_NAME.app" "$DMG_STAGING/"

# Add Application Shortcut
ln -s /Applications "$DMG_STAGING/Applications"

# Add Readme (Optional)
# cp README.md "$DMG_STAGING/"

# Create DMG file
hdiutil create -volname "$APP_NAME Installer" \
               -srcfolder "$DMG_STAGING" \
               -ov -format UDZO \
               "$OUTPUT_DMG"

# Cleanup Staging
rm -rf "$DMG_STAGING"

echo "---------------------------------------------------"
echo "[SUCCESS] Build Complete!"
echo "App Bundle: dist/$APP_NAME.app"
echo "Installer:  $OUTPUT_DMG"
echo "---------------------------------------------------"
