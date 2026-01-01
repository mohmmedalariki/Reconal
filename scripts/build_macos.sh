#!/bin/bash

# Navigate to project root (one level up from scripts/)
cd "$(dirname "$0")/.."

# Configuration
APP_NAME="Reconal"
MAIN_SCRIPT="src/reconal/app.py"
ICON_PNG="src/reconal/gui/assets/logo.png"
ICON_ICNS="Reconal.icns"
DIST_DIR="dist"
BUILD_DIR="build"

# 1. Cleanup
echo "[*] Cleaning up previous builds..."
rm -rf "$DIST_DIR" "$BUILD_DIR" "$APP_NAME.spec" "$ICON_ICNS" "Reconal_Installer.dmg"

# 2. Dependencies
echo "[*] Installing Project..."
pip install .

# 3. Icon Conversion (PNG -> ICNS)
if [ -f "$ICON_PNG" ]; then
    echo "[*] Converting icon..."
    mkdir Reconal.iconset
    sips -z 16 16     "$ICON_PNG" --out Reconal.iconset/icon_16x16.png
    sips -z 32 32     "$ICON_PNG" --out Reconal.iconset/icon_16x16@2x.png
    sips -z 32 32     "$ICON_PNG" --out Reconal.iconset/icon_32x32.png
    sips -z 64 64     "$ICON_PNG" --out Reconal.iconset/icon_32x32@2x.png
    sips -z 128 128   "$ICON_PNG" --out Reconal.iconset/icon_128x128.png
    sips -z 256 256   "$ICON_PNG" --out Reconal.iconset/icon_128x128@2x.png
    sips -z 256 256   "$ICON_PNG" --out Reconal.iconset/icon_256x256.png
    sips -z 512 512   "$ICON_PNG" --out Reconal.iconset/icon_256x256@2x.png
    sips -z 512 512   "$ICON_PNG" --out Reconal.iconset/icon_512x512.png
    sips -z 1024 1024 "$ICON_PNG" --out Reconal.iconset/icon_512x512@2x.png

    iconutil -c icns Reconal.iconset
    rm -rf Reconal.iconset
else
    echo "[!] Warning: $ICON_PNG not found. Using default icon."
fi

# 4. PyInstaller Bundle
echo "[*] Running PyInstaller..."
# Source: src/reconal/gui -> Destination: gui (inside the bundle)
# This places 'gui' folder at the root of sys._MEIPASS
pyinstaller --noconsole \
            --windowed \
            --name "$APP_NAME" \
            --icon "$ICON_ICNS" \
            --add-data "src/reconal/gui:gui" \
            "$MAIN_SCRIPT"

# 5. Create DMG (Optional but recommended for distribution)
if [ -d "dist/$APP_NAME.app" ]; then
    echo "[*] Creating DMG..."
    hdiutil create -volname "$APP_NAME" -srcfolder "dist/$APP_NAME.app" -ov -format UDZO "Reconal_Installer.dmg"
    echo "[+] Build Complete: Reconal_Installer.dmg"
else
    echo "[!] Build Failed: .app not found."
    exit 1
fi
