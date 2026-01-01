# Reconal Desktop App (macOS)

This document details how to build the native macOS Desktop version of Reconal using **PyWebView** and **PyInstaller**.

## 📂 Project Structure

-   `reconal_app.py`: Main entry point. Initializes the native window and bridges Python <-> JS.
-   `reconal_cli.py`: Core logic for modules and URL generation (reused).
-   `static/index.html`: The Dashboard UI (adapted for native use).
-   `static/icons/`: SVG icons for modules.
-   `build_macos.sh`: Automated build script.
-   `requirements_desktop.txt`: Python dependencies.

## 🛠 Prerequisites

1.  **Python 3.6+** installed.
2.  **pip** installed.
3.  **macOS** (for the `.app` and `.dmg` creation).

## 🚀 How to Build

We have provided a unified build script that handles dependency installation, icon conversion (`.png` -> `.icns`), bundling, and packaging.

1.  **Open a Terminal** in the project directory.
2.  **Run the build script**:
    ```bash
    chmod +x build_macos.sh
    ./build_macos.sh
    ```

### What the script does:
1.  Installs `pywebview` and `pyinstaller`.
2.  Converts `Reconal_icon.png` into a macOS-compatible `Reconal.icns` using `sips` and `iconutil`.
3.  Runs `PyInstaller` to create `dist/Reconal.app`.
    -   Bundles Python interpreter.
    -   Embeds `static/` website assets.
    -   Sets the application icon.
    -   Disables the console window (`--noconsole`).
4.  Runs `hdiutil` to package the `.app` into `Reconal_Installer.dmg`.

## 📦 Output

After a successful build, you will find:
-   **Executable Bundle**: `dist/Reconal.app` (You can drag this to Applications).
-   **Installer**: `Reconal_Installer.dmg` (Distributable disk image).

## 🔧 Running Locally (Development)

You can run the app without building it to test changes:

```bash
pip install -r requirements_desktop.txt
python3 reconal_app.py
```

*Note: In development mode, Debug Tools (Inspect Element) are enabled by default.*

## ⚠️ Troubleshooting

-   **"PyWebView not found"**: Ensure you ran `pip install -r requirements_desktop.txt`.
-   **Icon missing**: Ensure `Reconal_icon.png` is in the root directory before building.
-   **"System Events" error**: macOS might ask for permission to control UI elements during the build (rare, mostly for signing).
-   **App closes immediately**: Run the executable inside the bundle via terminal to see errors:
    ```bash
    ./dist/Reconal.app/Contents/MacOS/Reconal
    ```
