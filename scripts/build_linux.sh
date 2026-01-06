#!/bin/bash
# Reconal - Professional Linux Build Script

# 1. Setup Environment
set -e  # Exit on error
cd "$(dirname "$0")/.."  # Navigate to project root

APP_NAME="Reconal"
BINARY_NAME="Reconal_Linux"
ENTRY_POINT="src/reconal/app.py"
ICON_PATH="src/reconal/gui/assets/logo.png"

echo "============================================="
echo "   Building $APP_NAME for Linux (x64)       "
echo "============================================="

# 2. Cleanup
echo "[*] Cleaning up previous artifacts..."
rm -rf dist build "$APP_NAME.spec"

# 3. System Check (Optional warning)
if [ ! -f /etc/os-release ]; then
    echo "[!] Warning: Not running on standard Linux? Proceeding anyway..."
fi

# 4. Install Python Dependencies
echo "[*] Installing dependencies..."
pip install . 
pip install pyinstaller

# 5. Build Binary
echo "[*] Running PyInstaller..."
# --onefile: Create a single executable
# --noconsole: GUI application (no terminal popup)
# --add-data: Bundle the GUI assets
# --hidden-import: Ensure GTK libs are found if needed (typ. handled auto)

pyinstaller --noconsole \
            --onefile \
            --name "$BINARY_NAME" \
            --add-data "src/reconal/gui:gui" \
            "$ENTRY_POINT"

echo ""
echo "============================================="
if [ -f "dist/$BINARY_NAME" ]; then
    echo "✅ Build Success!"
    echo "   Binary Location: dist/$BINARY_NAME"
    echo "   Run with: ./dist/$BINARY_NAME"
else
    echo "❌ Build Failed."
    exit 1
fi
echo "============================================="
