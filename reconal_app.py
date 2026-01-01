import webview
import reconal_cli
import os
import sys
import webbrowser

class Api:
    def get_modules(self):
        """
        Returns list of modules with icon paths resolved relative to static/index.html
        """
        modules = reconal_cli.get_modules()
        clean_modules = []
        
        # Determine the path to icons (assuming we are running from project root)
        # When frozen (PyInstaller), we function inside sys._MEIPASS usually, or relative to executable
        # For development, we are at project root.
        # static/ is at root. 
        # index.html is in static/.
        # icons are in static/icons.
        # So relative path from index.html to icons is "icons/..."
        
        # We need to list files in static/icons dynamically.
        # Depending on how we run, absolute path to static folder changes.
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icons_dir = os.path.join(base_dir, 'static', 'icons')
        
        # PyInstaller handling
        if getattr(sys, 'frozen', False):
             base_dir = sys._MEIPASS
             icons_dir = os.path.join(base_dir, 'static', 'icons')

        available_icons = {}
        if os.path.exists(icons_dir):
            for f in os.listdir(icons_dir):
                if f.endswith(".svg"):
                    key = f.replace(".svg", "").lower()
                    # Path relative to static/index.html
                    available_icons[key] = f"icons/{f}"

        for m in modules:
            mod_data = {"name": m["name"]}
            name_norm = m["name"].lower().replace(" ", "")
            
            found_icon = None
            if name_norm in available_icons:
                found_icon = available_icons[name_norm]
            else:
                for key, path in available_icons.items():
                    if key in name_norm:
                        found_icon = path
                        break
            
            if found_icon:
                mod_data["customIcon"] = found_icon
            
            clean_modules.append(mod_data)
        
        return clean_modules

    def launch_module(self, index, target):
        """
        Launches the module at the given index against the target.
        Opens in the system default browser.
        """
        try:
            target = str(target).strip()
            index = int(index)
            
            if not target or index < 0:
                return {"status": "error", "message": "Invalid input"}

            modules = reconal_cli.get_modules()
            if index < len(modules):
                module = modules[index]
                url = module['url_func'](target)
                print(f"[*] Native Launch: {module['name']} -> {url}")
                # Open in system default browser (Chrome/Safari), NOT the webview window
                webbrowser.open(url)
                return {"status": "success", "url": url}
                
        except Exception as e:
            print(f"[!] Error handling launch: {e}")
        
        return {"status": "error"}

def main():
    api = Api()
    
    # Path to index.html
    if getattr(sys, 'frozen', False):
        # Running as compiled app
        html_path = os.path.join(sys._MEIPASS, 'static', 'index.html')
        debug_mode = False
    else:
        # Running as script
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'index.html')
        debug_mode = True

    window = webview.create_window(
        'Reconal', 
        html_path, 
        js_api=api,
        width=1200,
        height=900,
        resizable=True
    )
    
    webview.start(debug=debug_mode)

if __name__ == '__main__':
    main()
