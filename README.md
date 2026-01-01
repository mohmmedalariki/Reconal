# Reconal 🎯

**Reconal** is a professional-grade OSINT reconnaissance tool designed for Bug Bounty hunters and Security Researchers. It automates over **70+ advanced Google Dorks** and search queries through a sleek, native desktop interface.

![Banner](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)

## ✨ Features

-   **Native Desktop App**: Runs as a standalone window (macOS .app / Windows .exe) using PyWebView.
-   **Zero-Config Dashboard**: responsive, dark-themed UI that connects directly to the recon engine.
-   **70+ Recon Modules**:
    -   ☁️ **Cloud**: AWS S3, Azure Blob, Google Storage.
    -   🔌 **API**: Swagger, GraphQL, WSDL.
    -   🔓 **Leaks**: .env files, Pastebin, Trello, Source Maps.
    -   🛠 **DevOps**: Jenkins, Travis CI, .git folders.
    -   ⚡ **One-Click Launch**: Instantly opens targeted queries in your default browser.

## 📸 Screenshots

### Native Dashboard
![Dashboard](screenshots/dashboard.png)

### Advanced Modules
![Modules](screenshots/modules1.png)

## 🚀 Installation & Build

Reconal is now a **native desktop application**. You can download the pre-built binaries from the [Releases](https://github.com/mohmmedalariki/Reconal/releases) page, or build it yourself from source.

### 🍎 Build for macOS
Convert the python project into a native `.app` bundle and `.dmg` installer.
See: [**Build Guide for macOS**](docs/build_macos.md)

### 🪟 Build for Windows
Convert the project into a standalone `.exe`.
See: [**Build Guide for Windows**](docs/build_windows.md)

## 🛠 Usage

### Development Mode
You can run the app directly with Python if you prefer not to build the binary yet.
```bash
pip install .
python -m reconal.app
```

### CLI Support
Prefer the terminal? The legacy CLI tool works out of the box.
```bash
python reconal_cli.py -t example.com --list
```

## 🛡 Disclaimer
This tool is for educational and ethical testing purposes only. Usage for attacking targets without prior mutual consent is illegal. 
