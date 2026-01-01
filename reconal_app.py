import sys
import webbrowser
from pathlib import Path
from typing import List, Dict, Any, Optional

import webview
import reconal_cli


class BridgeApi:
    """Native API Bridge connecting Python backend to PyWebView frontend."""

    def __init__(self, static_dir: Path):
        self.static_dir = static_dir
        self.icons_dir = static_dir / "icons"

    def get_modules(self) -> List[Dict[str, Any]]:
        """
        Retrieves module list and maps custom icons via O(1) filesystem checks.
        """
        modules = reconal_cli.get_modules()
        
        # Optimize: Check for icons using O(1) direct path lookup
        # normalized_name -> path (e.g. "github" -> "icons/github.svg")
        cleaned_modules = []

        for m in modules:
            name_key = m["name"].lower().replace(" ", "")
            
            # Direct check: does icons/namekey.svg exist?
            icon_path = self.icons_dir / f"{name_key}.svg"
            
            mod_data = {"name": m["name"]}
            if icon_path.exists():
                mod_data["customIcon"] = f"icons/{name_key}.svg"
                
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
    static_path = base_path / "static"
    index_file = static_path / "index.html"

    if not index_file.exists():
        print(f"[!] Fatal: UI not found at {index_file}")
        sys.exit(1)

    api = BridgeApi(static_dir=static_path)
    
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
