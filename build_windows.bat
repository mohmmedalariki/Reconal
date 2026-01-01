@echo off
SETLOCAL
SET APP_NAME=Reconal
SET ICON_PNG=Reconal_icon.png
SET ICON_ICO=Reconal.ico
SET REQUIREMENTS=requirements_desktop.txt

echo [*] Starting Build Process for %APP_NAME% (Windows)...

:: 1. Check Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Python is not found in PATH. Please install Python 3.
    pause
    exit /b 1
)

:: 2. Install Dependencies
echo [*] Installing Dependencies from %REQUIREMENTS%...
pip install -r %REQUIREMENTS%
:: Ensure Pillow is installed for icon conversion
pip install Pillow

:: 3. Convert Icon (PNG -> ICO) using Python
echo [*] Checking Icon...
IF EXIST "%ICON_PNG%" (
    echo     Found %ICON_PNG%. Converting to %ICON_ICO%...
    python -c "from PIL import Image; img = Image.open('%ICON_PNG%'); img.save('%ICON_ICO%', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])"
) ELSE (
    echo [!] %ICON_PNG% not found. Simple conversion skipped.
)

:: 4. Clean previous builds
echo [*] Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q %APP_NAME%.spec 2>nul

:: 5. Run PyInstaller
echo [*] Running PyInstaller...
:: --noconsole: Startup without cmd window
:: --onefile: Bundle everything into a single .exe
:: --windowed: Same as noconsole
:: --add-data: Syntax for Windows is source;dest
pyinstaller --noconsole ^
            --onefile ^
            --windowed ^
            --name "%APP_NAME%" ^
            --icon "%ICON_ICO%" ^
            --add-data "static;static" ^
            reconal_app.py

IF NOT EXIST "dist\%APP_NAME%.exe" (
    echo [!] Build Failed! Check errors above.
    pause
    exit /b 1
)

echo ---------------------------------------------------
echo [SUCCESS] Build Complete!
echo Executable: dist\%APP_NAME%.exe
echo ---------------------------------------------------
pause
