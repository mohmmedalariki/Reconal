@echo off
:: Navigate to project root (one level up from scripts/)
cd /d "%~dp0.."

:: Configuration
set APP_NAME=Reconal
set MAIN_SCRIPT=src\reconal\app.py
set ICON_PNG=src\reconal\gui\assets\logo.png
set ICON_ICO=Reconal.ico

:: 1. Cleanup
echo [*] Cleaning up...
rmdir /s /q dist build
del /q *.spec

:: 2. Dependencies
echo [*] Installing Project...
pip install .

:: 3. Icon Conversion
echo [*] Converting Icon...
if exist "%ICON_PNG%" (
    python -c "from PIL import Image; img = Image.open(r'%ICON_PNG%'); img.save(r'%ICON_ICO%', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])"
) else (
    echo [!] Warning: Icon not found at %ICON_PNG%
)

:: 5. Run PyInstaller
echo [*] Running PyInstaller...
:: Source: src\reconal\gui -> Destination: gui
pyinstaller --noconsole ^
            --onefile ^
            --windowed ^
            --name "%APP_NAME%" ^
            --icon "%ICON_ICO%" ^
            --add-data "src\reconal\gui;gui" ^
            "%MAIN_SCRIPT%"
