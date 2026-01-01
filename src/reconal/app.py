import webbrowser
from pathlib import Path
from typing import List, Dict, Any, Optional

import webview
from . import cli as reconal_cli  # Relative import for package structure


class BridgeApi:
    """Native API Bridge connecting Python backend to PyWebView frontend."""

    def __init__(self, gui_dir: Path):
        self.gui_dir = gui_dir
        self.assets_dir = gui_dir / "assets"

    def get_modules(self) -> List[Dict[str, Any]]:
        """
        Retrieves module list and maps custom icons via O(1) filesystem checks.
        """
        modules = reconal_cli.get_modules()
        
        # Optimize: Check for icons using O(1) direct path lookup
        # normalized_name -> path (e.g. "github" -> "assets/github.svg")
        cleaned_modules = []

        for m in modules:
            name_key = m["name"].lower().replace(" ", "")
            
            # Direct check: does assets/namekey.svg exist?
            icon_path = self.assets_dir / f"{name_key}.svg"
            
            mod_data = {"name": m["name"]}
            if icon_path.exists():
                mod_data["customIcon"] = f"assets/{name_key}.svg"
                
            cleaned_modules.append(mod_data)

        return cleaned_modules

    def launch_module(self, index: int, target: str) -> Dict[str, str]:
        """Launches the selected module in the system default browser."""
        try:
            target = str(target).strip()
            if not target or index < 0:
                return {"status": "error", "message": "Invalid input"}

            modules = reconal_cli.get_modules()
            if index < len(modules):
                module = modules[index]
                url = module['url_func'](target)
                
                print(f"[*] Opening: {module['name']}")
                webbrowser.open(url)
                return {"status": "success", "url": url}
                
        except Exception as e:
            print(f"[!] Launch Error: {e}")
        
        return {"status": "error"}


def get_resource_path() -> Path:
    """Returns the absolute path to resources, handling PyInstaller's sys._MEIPASS."""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent.resolve()


def main() -> None:
    """Application Entry Point."""
    base_path = get_resource_path()
    
    # In src layout, this file is in src/reconal/app.py
    # Debug mode: base_path is src/reconal/
    # Frozen mode: base_path is temp/_MEIPASS/reconal (if we bundle correctly)
    
    gui_path = base_path / "gui"
    index_file = gui_path / "index.html"

    if not index_file.exists():
        # Fallback for dev mode if we are running from root
        # If running from root as `python -m src.reconal.app`
        if (Path.cwd() / "src/reconal/gui").exists():
             gui_path = Path.cwd() / "src/reconal/gui"
             index_file = gui_path / "index.html"

    if not index_file.exists():
        print(f"[!] Fatal: UI not found at {index_file}")
        sys.exit(1)

    api = BridgeApi(gui_dir=gui_path)
    
    # Initialize Native Window
    webview.create_window(
        title='Reconal',
        url=str(index_file),
        js_api=api,
        width=1200,
        height=900,
        resizable=True,
        text_select=False
    )
    
    webview.start(debug=not getattr(sys, 'frozen', False))


if __name__ == '__main__':
    main()
