#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import urllib.parse
import json
import reconal_cli
import threading
import time
import sys
import os

PORT = 8080

# --- Embedded Frontend ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reconal | Dashboard</title>
    <style>
        :root {
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --accent: #2ea043;
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --border: #30363d;
            --glow: rgba(46, 160, 67, 0.4);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        header {
            width: 100%;
            padding: 2rem 0;
            text-align: center;
            background: linear-gradient(180deg, #161b22 0%, var(--bg-color) 100%);
            border-bottom: 1px solid var(--border);
            margin-bottom: 2rem;
        }

        h1 {
            margin: 0;
            font-size: 2.5rem;
            color: var(--text-main);
            letter-spacing: -1px;
        }

        .highlight {
            color: var(--accent);
            text-shadow: 0 0 15px var(--glow);
        }

        .container {
            width: 90%;
            max-width: 1200px;
            margin-bottom: 3rem;
        }

        /* Search Section */
        .search-box {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            display: flex;
            gap: 1rem;
            align-items: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        input[type="text"] {
            flex: 1;
            background: #0d1117;
            border: 1px solid var(--border);
            color: white;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 1.1rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        input[type="text"]:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(46, 160, 67, 0.2);
        }

        .status {
            font-size: 0.9rem;
            color: var(--text-muted);
        }

        /* Module Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.25rem;
            cursor: pointer;
            transition: transform 0.2s, border-color 0.2s, background 0.2s;
            position: relative;
            overflow: hidden;
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: var(--accent);
            background: #1c2128;
        }

        .card h3 {
            margin: 0 0 0.5rem 0;
            font-size: 1.1rem;
            font-weight: 600;
        }

        .card p {
            margin: 0;
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.4;
        }

        .icon-box {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            background: rgba(255,255,255,0.03);
            border-radius: 6px;
        }

        .icon-svg {
            width: 20px !important;
            height: 20px !important;
            min-width: 20px;
            min-height: 20px;
            object-fit: contain;
            fill: var(--text-muted);
            transition: fill 0.2s;
            display: block;
            margin: 0 !important;
        }

        /* Notification Toast */
        #toast {
            visibility: hidden;
            min-width: 250px;
            background-color: var(--accent);
            color: white;
            text-align: center;
            border-radius: 8px;
            padding: 16px;
            position: fixed;
            z-index: 1;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            font-weight: 600;
        }

        #toast.show {
            visibility: visible;
            animation: fadein 0.5s, fadeout 0.5s 2.5s;
        }

        @keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }

        @keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 0; opacity: 0;}
        }
    </style>
</head>
<body>

    <header>
        <h1>Recon<span class="highlight">al</span></h1>
        <p style="color: var(--text-muted);">Pro Reconnaissance Dashboard</p>
    </header>

    <div class="container">
        
        <div class="search-box">
            <span style="font-size: 1.5rem;">🎯</span>
            <input type="text" id="target" placeholder="Enter Target Domain (e.g., example.com)" autofocus>
            <div class="status" id="target-status">Waiting for input...</div>
        </div>

        <div class="grid" id="module-grid">
            <!-- Cards will be injected here by JS -->
        </div>

    </div>

    <div id="toast">Launched Module!</div>

    <script>
        let modules = [];
        const grid = document.getElementById('module-grid');
        const targetInput = document.getElementById('target');
        const statusLabel = document.getElementById('target-status');

        // Fetch modules from Python backend
        async function fetchModules() {
            const response = await fetch('/api/modules');
            modules = await response.json();
            renderGrid(modules);
        }

        function getSimpleIcon(name) {
            // Safety check
            if (typeof SimpleIcons === 'undefined') return null;

            // 1. Try manual map
            for (const [key, slug] of Object.entries(iconMap)) {
                if (name.includes(key) && SimpleIcons[slug]) {
                    return SimpleIcons[slug];
                }
            }
            
            // 2. Fallbacks
            if (name.includes("Database")) return SimpleIcons.siDatabricks; 
            if (name.includes("Config")) return SimpleIcons.siCodeigniter;
            if (name.includes("Login")) return SimpleIcons.siAuth0;
            
            // 3. Default
            return SimpleIcons.siGoogle; 
        }

        // Emoji Fallback Map
        const emojiMap = {
            "Directory": "📂",
            "Config": "⚙️",
            "Database": "🗄️",
            "SQL": "💉",
            "Log": "📝",
            "Backup": "💾",
            "Login": "🔐",
            "Documents": "📄",
            "PHP": "🐘",
            "Backdoor": "☠️",
            "Shell": "🐚",
            "Install": "💿",
            "Redirect": "➡️",
            "Header": "🛡️",
            "Robots": "🤖",
            "Crossdomain": "❌",
            "Subdomain": "🌐",
            "Buckets": "🪣", 
            "Spaces": "☁️",
            "Environment": "🌿",
            "Source Map": "🗺️",
            "Traefik": "🚦",
            "WhatCMS": "❓",
            "Throwbin": "🗑️",
            "Pastebin": "📋",
            "CRT": "📜",
            "IP": "📍",
            "Domain": "🏠"
        };

        function getEmojiIcon(name) {
            for (const [key, emoji] of Object.entries(emojiMap)) {
                if (name.includes(key)) {
                    return emoji;
                }
            }
            return null;
        }

        function renderGrid(mods) {
            grid.innerHTML = '';
            mods.forEach((mod, index) => {
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => launchModule(index);
                
                let iconHtml = '';

                // 1. Check for Custom Icon (Served from Backend)
                if (mod.customIcon) {
                     iconHtml = `<img src="${mod.customIcon}" class="icon-svg" alt="${mod.name}">`;
                } else {
                    // 2. Check for SimpleIcons
                    let iconObj = null;
                    try {
                        iconObj = getSimpleIcon(mod.name);
                    } catch (e) { console.error(e); }

                    if (iconObj) {
                        let svgContent = iconObj.svg;
                        svgContent = svgContent.replace('<svg', '<svg class="icon-svg"');
                        iconHtml = svgContent;
                    } else {
                        // 3. Check for Emoji Fallback
                        const emoji = getEmojiIcon(mod.name);
                        if (emoji) {
                            // Render emoji centered in the box
                            iconHtml = `<span style="font-size: 1.25rem; line-height: 1;">${emoji}</span>`;
                        } else {
                            // 4. Final Generic Fallback
                           iconHtml = '<svg class="icon-svg" viewBox="0 0 24 24"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>';
                        }
                    }
                }

                card.innerHTML = `
                    <div class="card-header">
                        <div class="icon-box">
                            ${iconHtml}
                        </div>
                        <h3>${mod.name}</h3>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        async function launchModule(index) {
            const target = targetInput.value.trim();
            if (!target) {
                showToast("⚠️ Enter a target domain first!");
                targetInput.focus();
                targetInput.style.borderColor = "#f85149";
                setTimeout(() => targetInput.style.borderColor = "#30363d", 1000);
                return;
            }

            showToast(`🚀 Launching: ${modules[index].name}`);
            
            // Call backend to open URL
            await fetch(`/api/launch?index=${index}&target=${encodeURIComponent(target)}`);
        }

        function showToast(message) {
            const x = document.getElementById("toast");
            x.innerText = message;
            x.className = "show";
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
        }

        // Input handler
        targetInput.addEventListener('input', (e) => {
            if (e.target.value.length > 3) {
                statusLabel.innerText = "Target Set: " + e.target.value;
                statusLabel.style.color = "var(--accent)";
            } else {
                statusLabel.innerText = "Waiting for input...";
                statusLabel.style.color = "var(--text-muted)";
            }
        });

        // Initial Load
        fetchModules();

    </script>
</body>
</html>
"""

class ReconHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
            return

        elif parsed_path.path.startswith("/static/"):
            # Serve static files securely
            safe_path = os.path.normpath(parsed_path.path).lstrip('/')
            if not safe_path.startswith("static/"):
                self.send_error(403)
                return
            if os.path.exists(safe_path) and os.path.isfile(safe_path):
                super().do_GET() 
            else:
                self.send_error(404)
            return

        elif parsed_path.path == "/api/modules":
            modules = reconal_cli.get_modules()
            clean_modules = []
            
            # Map available custom icons
            available_icons = {}
            if os.path.exists("static/icons"):
                for f in os.listdir("static/icons"):
                    if f.endswith(".svg"):
                        # Key = filename without extension (e.g. 'microsoftsharepoint')
                        key = f.replace(".svg", "").lower()
                        available_icons[key] = f"static/icons/{f}"

            for m in modules:
                mod_data = {"name": m["name"]}
                # Normalize module name for matching: lowercase and remove spaces
                # e.g. "Microsoft SharePoint" -> "microsoftsharepoint"
                name_norm = m["name"].lower().replace(" ", "")
                
                # Try to find a matching custom icon
                found_icon = None
                
                # 1. Exact match against normalized name (e.g. microsoftsharepoint == microsoftsharepoint)
                if name_norm in available_icons:
                    found_icon = available_icons[name_norm]
                else:
                    # 2. Key inclusion match (e.g. 'shodan' inside 'shodansearch')
                    for key, path in available_icons.items():
                        if key in name_norm:
                            found_icon = path
                            break
                
                if found_icon:
                    mod_data["customIcon"] = found_icon
                
                clean_modules.append(mod_data)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(clean_modules).encode('utf-8'))
            return

        elif parsed_path.path == "/api/launch":
            query = urllib.parse.parse_qs(parsed_path.query)
            try:
                target = query.get('target', [''])[0]
                index = int(query.get('index', [-1])[0])
                
                if target and index >= 0:
                    modules = reconal_cli.get_modules()
                    if index < len(modules):
                        module = modules[index]
                        url = module['url_func'](target)
                        print(f"[*] API Launch: {module['name']} -> {url}")
                        webbrowser.open_new_tab(url)
                        
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "success", "url": url}).encode('utf-8'))
                        return
            except Exception as e:
                print(f"[!] Error handling launch: {e}")
            
            self.send_response(400)
            self.end_headers()
            return

        else:
            # Fallback for favicon etc.
            super().do_GET()

    def log_message(self, format, *args):
        # Silence logs to keep terminal clean
        return

def open_browser():
    time.sleep(1)
    print(f"[*] Opening browser at http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}")

def main():
    global PORT
    print(f"[*] Starting Reconal Web Server...")
    print(f"[*] Use Ctrl+C to stop.")
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    # Dynamic Port Allocation
    while True:
        try:
            with socketserver.TCPServer(("", PORT), ReconHandler) as httpd:
                print(f"[*] Serving on http://localhost:{PORT}")
                # Launch browser in background
                threading.Thread(target=open_browser, daemon=True).start()
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n[*] Stopping server...")
                    httpd.shutdown()
                break # Exit loop on successful run
        except OSError as e:
            if e.errno == 48: # Address already in use
                print(f"[!] Port {PORT} is busy, trying {PORT + 1}...")
                PORT += 1
                if PORT > 8100:
                    print("[!] Could not find an open port in range 8080-8100.")
                    sys.exit(1)
            else:
                raise e

if __name__ == "__main__":
    main()
