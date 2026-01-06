# Build Guide for Linux 🐧

Reconal supports Linux through a standalone binary build using PyInstaller.
Since Linux distributions vary, we provide a build script that works on most major distributions (Ubuntu, Debian, Fedora, Arch).

## Prerequisites

You need **Python 3.8+** and the system libraries required by **PyWebView** (WebKit2GTK).

### 1. Install System Dependencies

**Ubuntu / Debian / Kali:**
```bash
sudo apt-get update
sudo apt-get install python3-pip libgtk-3-dev libwebkit2gtk-4.0-dev
```

**Fedora:**
```bash
sudo dnf install python3-pip gtk3-devel webkit2gtk3-devel
```

**Arch Linux:**
```bash
sudo pacman -S python-pip gtk3 webkit2gtk
```

---

## Build Steps

We provide an automated script to handle the build process.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/mohmmedalariki/Reconal.git
    cd Reconal
    ```

2.  **Run the Build Script**:
    ```bash
    ./scripts/build_linux.sh
    ```

3.  **Run the App**:
    The binary will be created in the `dist/` folder.
    ```bash
    ./dist/Reconal_Linux
    ```

---

## Troubleshooting

*   **"Module Not Found"**: Ensure you ran the script from the root (or let the script handle it) and that `pip` successfully installed dependencies.
*   **GTK/WebKit Errors**: If the app launches but shows a blank window or crashes, ensure `libwebkit2gtk` is installed.
*   **Wayland Issues**: PyWebView is generally stable on X11. If you have issues on Wayland, try enforcing X11: `GDK_BACKEND=x11 ./dist/Reconal_Linux`.
