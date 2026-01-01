# Reconal Desktop (Windows)

This document details how to build the native Windows Desktop version of Reconal. 
The application will run as a standalone `.exe` using Microsoft Edge WebView2.

## 🛠 Prerequisites

1.  **Windows 10 or 11**.
2.  **Python 3.7+** installed and added to PATH.
3.  **WebView2 Runtime**: Included by default on Windows 11 and updated Windows 10. If missing, the app may prompt to install it or fail silently depending on the system.

## 🚀 How to Build

We have provided a batch script (`build_windows.bat`) to automate the process.

1.  Open Command Prompt or PowerShell in the project directory.
2.  Run the build script:
    ```cmd
    build_windows.bat
    ```

### What the script does:
1.  Installs dependencies (`pywebview`, `pyinstaller`, `Pillow`).
2.  Converts `Reconal_icon.png` to `Reconal.ico` automatically using Python.
3.  Runs PyInstaller with:
    -   `--onefile`: Creates a single `.exe` file.
    -   `--noconsole`: Hides the terminal window.
    -   `--add-data "static;static"`: Bundles the UI files.

## 📦 Output

After a successful build, check the `dist` folder:
-   **`dist\Reconal.exe`** (Standalone executable)

## ⚠️ Common Windows Issues

### 1. Windows Defender SmartScreen
When you run the `.exe` for the first time on a new PC, Windows SmartScreen will likely block it because it is an **unsigned** application.
-   **Fix**: Click **"More info"** -> **"Run anyway"**.

### 2. "PyWebView" or DLL Errors
-   Ensure you have the [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) installed.
-   If `pywebview` fails to find a renderer, it usually means WebView2 is missing.

### 3. Icon not showing
-   Windows caches icons aggressively. Move the `.exe` to a different folder to force an icon refresh.

### 4. Port Conflicts?
-   Likely none. This version does **not** rely on `http.server` or port 8080. It interacts directly with the Python process via memory.
