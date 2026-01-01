#!/usr/bin/env python3
"""
Reconal CLI: Advanced OSINT Reconnaissance Tool
Core logic and command-line interface.
"""
import argparse
import sys
import urllib.parse
import webbrowser
import time
from typing import List, Dict, Callable, Any, TypedDict

BANNER = r"""
  _____                      _ 
 |  __ \                    | |
 | |__) |___  ___ ___  _ __ | |
 |  _  // _ \/ __/ _ \| '_ \| |
 | | \ \  __/ (_| (_) | | | | |
 |_|  \_\___|\___\___/|_| |_|_|
                               
          Reconal CLI
"""

class ReconModule(TypedDict):
    name: str
    url_func: Callable[[str], str]
    customIcon: str

def _google_search(query: str) -> str:
    """Helper to generate a Google search URL."""
    return f"https://www.google.com/search?q={query}"

def get_modules() -> List[Dict[str, Any]]:
    """Generates the list of available reconnaissance modules."""
    
    def q(text: str) -> str:
        return urllib.parse.quote(text)

    modules = [
        # --- File Discovery ---
        {
            "name": "Directory Listing",
            "url_func": lambda t: _google_search(f"site:{q(t)} intitle:index.of")
        },
        {
            "name": "Configuration Files",
            "url_func": lambda t: _google_search(f"site:{q(t)} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini")
        },
        {
            "name": "Database Files",
            "url_func": lambda t: _google_search(f"site:{q(t)} ext:sql | ext:dbf | ext:mdb")
        },
        {
            "name": "Log Files",
            "url_func": lambda t: _google_search(f"site:{q(t)} ext:log")
        },
        {
            "name": "Backup Files",
            "url_func": lambda t: _google_search(f"site:{q(t)} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup")
        },
        
        # --- Platform Specific ---
        {
            "name": "WordPress Core",
            "url_func": lambda t: _google_search(f"site:{q(t)} inurl:wp- | inurl:wp-content | inurl:plugins | inurl:uploads | inurl:themes | inurl:download")
        },
        {
            "name": "Apache Configs",
            "url_func": lambda t: _google_search(f"site:{q(t)} filetype:config \"apache\"")
        },
        {
            "name": "Apache Struts",
            "url_func": lambda t: _google_search(f"site:{q(t)} ext:action | ext:struts | ext:do")
        },
        {
            "name": "Jenkins Instances",
            "url_func": lambda t: _google_search(f"intitle:\"Dashboard [Jenkins]\" \"{q(t)}\"")
        },
        {
             "name": "Traefik Dashboard",
             "url_func": lambda t: _google_search(f"intitle:traefik inurl:8080/dashboard \"{q(t)}\"")
        },

        # --- Sensitive Information ---
        {
            "name": "Login Pages",
            "url_func": lambda t: _google_search(f"site:{q(t)} inurl:login | inurl:signin | intitle:Login | intitle: signin | inurl:auth")
        },
        {
            "name": "PHP Errors",
            "url_func": lambda t: _google_search(f"site:{q(t)} ext:php intitle:phpinfo \"published by the PHP Group\"")
        },
        {
            "name": "SQL Injection Errors",
            "url_func": lambda t: _google_search(f"site:{q(t)} intext:\"sql syntax near\" | intext:\"syntax error has occurred\" | intext:\"incorrect syntax near\" | intext:\"unexpected end of SQL command\"")
        },
        {
            "name": "Open Redirects",
            "url_func": lambda t: _google_search(f"site:{q(t)} inurl:redir | inurl:url | inurl:redirect | inurl:return | inurl:src=http | inurl:r=http")
        },
        {
            "name": ".env Files",
            "url_func": lambda t: _google_search(f"site:{q(t)} filename:.env | filename:env | inurl:env")
        },
        {
            "name": "Git Folders",
            "url_func": lambda t: _google_search(f"inurl:\"/.git\" {q(t)} -github")
        },

        # --- External Services ---
        {
            "name": "Pastebin Search",
            "url_func": lambda t: _google_search(f"site:pastebin.com {q(t)}")
        },
        {
            "name": "LinkedIn Employees",
            "url_func": lambda t: _google_search(f"site:linkedin.com employees {q(t)}")
        },
        {
            "name": "Github Search",
            "url_func": lambda t: f"https://github.com/search?q=\"*.{q(t)}\""
        },
        {
            "name": "StackOverflow Support",
            "url_func": lambda t: _google_search(f"site:stackoverflow.com \"{q(t)}\"")
        },
        {
            "name": "Trello Boards",
            "url_func": lambda t: _google_search(f"site:trello.com \"{q(t)}\"")
        },
        {
            "name": "S3 Buckets",
            "url_func": lambda t: _google_search(f"site:.s3.amazonaws.com \"{q(t)}\"")
        },
        {
            "name": "DigitalOcean Spaces",
            "url_func": lambda t: _google_search(f"site:digitaloceanspaces.com \"{q(t)}\"")
        },

        # --- Network & DNS ---
        {
            "name": "CRT.sh",
            "url_func": lambda t: f"https://crt.sh/?q={q(t)}"
        },
        {
            "name": "Shodan",
            "url_func": lambda t: f"https://www.shodan.io/search?query={q(t)}"
        },
        {
            "name": "Security Headers",
            "url_func": lambda t: f"https://securityheaders.com/?q={q(t)}&followRedirects=on"
        },
        {
            "name": "Wayback Machine",
            "url_func": lambda t: f"https://web.archive.org/web/*/{q(t)}/*"
        },
        
        # --- API Intelligence ---
        {
            "name": "Swagger/OpenAPI",
            "url_func": lambda t: _google_search(f"site:{q(t)} inurl:swagger | inurl:api-docs | inurl:v1/api | inurl:\"/v2/api-docs\"")
        },
        {
             "name": "GraphQL Endpoints",
             "url_func": lambda t: _google_search(f"site:{q(t)} inurl:graphql | inurl:graphiql | intext:\"query {{\\\"")
        },
        {
             "name": "Postman Collections",
             "url_func": lambda t: _google_search(f"site:postman.com \"{q(t)}\"")
        }
    ]
    return modules

def main() -> None:
    parser = argparse.ArgumentParser(description="Reconal CLI: Professional OSINT Tool")
    parser.add_argument("-t", "--target", help="Target domain (e.g., example.com)")
    parser.add_argument("-l", "--list", action="store_true", help="List available modules")
    parser.add_argument("-a", "--all", action="store_true", help="Execute ALL modules (Caution: Opens many tabs)")
    parser.add_argument("-i", "--index", type=int, help="Run specific module index (1-based)")
    
    args = parser.parse_args()
    print(BANNER)

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    modules = get_modules()

    if args.list:
        print(f"Available Modules for: {args.target or '<target>'}")
        print("-" * 60)
        for i, m in enumerate(modules, 1):
            print(f"{i:>3}. {m['name']}")
        print("-" * 60)
        return

    if not args.target:
        print("[!] Error: Target domain required (-t)")
        sys.exit(1)

    if args.index:
        if 1 <= args.index <= len(modules):
            mod = modules[args.index - 1]
            url = mod['url_func'](args.target)
            print(f"[*] Launching: {mod['name']}")
            print(f"    URL: {url}")
            webbrowser.open(url)
        else:
            print(f"[!] Invalid index. Choose 1-{len(modules)}")
            
    elif args.all:
        print(f"[!] Warning: Launching {len(modules)} tabs.")
        if input("Continue? (y/n): ").lower() == 'y':
            for mod in modules:
                url = mod['url_func'](args.target)
                print(f"[*] {mod['name']}...")
                webbrowser.open(url)
                time.sleep(0.5)

if __name__ == "__main__":
    main()
