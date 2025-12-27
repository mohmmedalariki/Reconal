#!/usr/bin/env python3
import argparse
import sys
import urllib.parse
import webbrowser
import time

# ASCII Banner
BANNER = r"""
  _____                      _ 
 |  __ \                    | |
 | |__) |___  ___ ___  _ __ | |
 |  _  // _ \/ __/ _ \| '_ \| |
 | | \ \  __/ (_| (_) | | | | |
 |_|  \_\___|\___\___/|_| |_|_|
                               
          Reconal CLI
"""

def get_modules():
    """
    Returns a list of dictionaries, each representing a search module.
    Keys: 'name', 'template' (url string with placeholder)
    """
    # Helper for quoting strings in search queries
    # In C#, HttpUtility.UrlEncode is used on the input.
    # We will format the string first, then encode the user input part.
    
    modules = [
        {
            "name": "Directory Listing",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} intitle:index.of"
        },
        {
            "name": "Configuration Files (xml, conf, cnf, reg, inf, rdp, cfg, txt, ora, ini)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini"
        },
        {
            "name": "Database Files (sql, dbf, mdb)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:sql | ext:dbf | ext:mdb"
        },
        {
            "name": "WordPress (wp-, plugins, uploads, themes)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:wp- | inurl:wp-content | inurl:plugins | inurl:uploads | inurl:themes | inurl:download"
        },
        {
            "name": "Log Files",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:log"
        },
        {
            "name": "Backup Files (bkf, bkp, bak, old, backup)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup"
        },
        {
            "name": "Login Pages",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:login | inurl:signin | intitle:Login | intitle: signin | inurl:auth"
        },
        {
            "name": "Documents (doc, docx, odt, pdf, rtf, ppt, csv, etc.)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv"
        },
        {
            "name": "PHP Errors / Info",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:php intitle:phpinfo \"published by the PHP Group\""
        },
        {
            "name": "Backdoors & Shells",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:shell | inurl:backdoor | inurl:wso | inurl:cmd | shadow | passwd | boot.ini | inurl:backdoor"
        },
        {
            "name": "Install / Setup / Readme",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:readme | inurl:license | inurl:install | inurl:setup | inurl:config"
        },
        {
            "name": "SQL Injection Errors",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} intext:\"sql syntax near\" | intext:\"syntax error has occurred\" | intext:\"incorrect syntax near\" | intext:\"unexpected end of SQL command\" | intext:\"Warning: mysql_connect()\" | intext:\"Warning: mysql_query()\" | intext:\"Warning: pg_connect()\""
        },
        {
            "name": "Open Redirects",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:redir | inurl:url | inurl:redirect | inurl:return | inurl:src=http | inurl:r=http"
        },
        {
            "name": "Apache Struts / Actions",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:action | ext:struts | ext:do"
        },
        {
            "name": "Pastebin Search",
            "url_func": lambda t: f"https://www.google.com/search?q=site:pastebin.com {urllib.parse.quote(t)}"
        },
        {
            "name": "LinkedIn Employees",
            "url_func": lambda t: f"https://www.google.com/search?q=site:linkedin.com employees {urllib.parse.quote(t)}"
        },
        {
            "name": "SharePoint",
            "url_func": lambda t: f"https://www.google.com/search?q=.sharepoint.com/_vti_bin/webpartpages/asmx -docs -msdn -mdsec site:{urllib.parse.quote(t)}"
        },
        {
            "name": ".NET / WSDL / SOAP",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} filetype:wsdl | filetype:WSDL | ext:svc | inurl:wsdl | Filetype: ?wsdl | inurl:asmx?wsdl | inurl:jws?wsdl | intitle:_vti_bin/sites.asmx?wsdl | inurl:_vti_bin/sites.asmx?wsdl"
        },
        {
            "name": "Github Search",
            "url_func": lambda t: f"https://github.com/search?q=\"*.{urllib.parse.quote(t)}\""
        },
        {
            "name": "Github Gist Search",
            "url_func": lambda t: f"https://gist.github.com/search?q=*.{urllib.parse.quote(t)}"
        },
        {
            "name": "Apache Configs",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} filetype:config \"apache\""
        },
        {
            "name": "Code Leaks (Pastebin, JSFiddle, etc.)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:http://ideone.com | site:http://codebeautify.org | site:http://codeshare.io | site:http://codepen.io | site:http://repl.it | site:http://justpaste.it | site:http://pastebin.com | site:http://jsfiddle.net | site:http://trello.com | site:*.atlassian.net | site:bitbucket.org \"{urllib.parse.quote(t)}\""
        },
        {
            "name": "Atlassian / Bitbucket",
            "url_func": lambda t: f"https://www.google.com/search?q=site:atlassian.net | site:bitbucket.org \"{urllib.parse.quote(t)}\""
        },
        {
            "name": ".git Folders",
            "url_func": lambda t: f"https://www.google.com/search?q=inurl:\"/.git\" {urllib.parse.quote(t)} -github"
        },
        {
            "name": "Traefik Dashboard",
            "url_func": lambda t: f"https://www.google.com/search?q=intitle:traefik inurl:8080/dashboard \"{urllib.parse.quote(t)}\""
        },
        {
            "name": "CRT.sh (Certificate Search)",
            "url_func": lambda t: f"https://crt.sh/?q={urllib.parse.quote(t)}"
        },
        {
            "name": "PHPInfo / .htaccess",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:\"/phpinfo.php\" | inurl:\".htaccess\""
        },
        {
            "name": "Subdomains (*.target.com)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:*.{urllib.parse.quote(t)}"
        },
        {
            "name": "Sub-Subdomains (*.*.target.com)",
            "url_func": lambda t: f"https://www.google.com/search?q=site:*.*.{urllib.parse.quote(t)}"
        },
        {
            "name": "WordPress Content/Includes",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:wp-content | inurl:wp-includes"
        },
        {
            "name": "Wayback Machine (WordPress)",
            "url_func": lambda t: f"http://wwwb-dedup.us.archive.org:8083/cdx/search?url={urllib.parse.quote(t)}/&matchType=domain&collapse=digest&output=text&fl=original,timestamp&filter=urlkey:.*wp[-].*&limit=1000000&xx="
        },
        {
            "name": "OpenBugBounty",
            "url_func": lambda t: f"https://www.openbugbounty.org/search/?search={urllib.parse.quote(t)}"
        },
        {
            "name": "Reddit Search",
            "url_func": lambda t: f"https://www.reddit.com/search/?q={urllib.parse.quote(t)}"
        },
        {
            "name": "Crossdomain.xml",
            "url_func": lambda t: f"https://www.google.com/search?q={urllib.parse.quote(t)}/crossdomain.xml"
        },
        {
            "name": "Robots.txt",
            "url_func": lambda t: f"https://www.google.com/search?q={urllib.parse.quote(t)}/robots.txt"
        },
        {
            "name": "Security Headers",
            "url_func": lambda t: f"https://securityheaders.com/?q={urllib.parse.quote(t)}&followRedirects=on"
        },
        {
            "name": "ThreatCrowd",
            "url_func": lambda t: f"https://threatcrowd.org/domain.php?domain={urllib.parse.quote(t)}"
        },
        {
            "name": "RiskIQ",
            "url_func": lambda t: f"https://community.riskiq.com/search/{urllib.parse.quote(t)}"
        },
        {
            "name": "SWF Files (Google)",
            "url_func": lambda t: f"https://www.google.com/search?q=inurl:{urllib.parse.quote(t)} ext:swf"
        },
        {
            "name": "YouTube Search",
            "url_func": lambda t: f"https://www.youtube.com/results?search_query={urllib.parse.quote(t)}"
        },
        {
            "name": "Yandex SWF",
            "url_func": lambda t: f"https://yandex.com/search/?text=site:{urllib.parse.quote(t)} mime:swf"
        },
        {
            "name": "Wayback Machine SWF",
            "url_func": lambda t: f"https://web.archive.org/cdx/search?url={urllib.parse.quote(t)}/&matchType=domain&collapse=urlkey&output=text&fl=original&filter=urlkey:.*swf&limit=100000"
        },
        {
            "name": "Wayback Machine MIME SWF",
            "url_func": lambda t: f"https://web.archive.org/cdx/search?url={urllib.parse.quote(t)}/&matchType=domain&collapse=urlkey&output=text&fl=original&filter=mimetype:application/x-shockwave-flash&limit=100000"
        },
        {
            "name": "Wayback Machine (All)",
            "url_func": lambda t: f"https://web.archive.org/web/*/{urllib.parse.quote(t)}/*"
        },
        {
            "name": "Reverse IP (ViewDNS)",
            "url_func": lambda t: f"https://viewdns.info/reverseip/?host={urllib.parse.quote(t)}&t=1"
        },
        {
            "name": "PublicWWW",
            "url_func": lambda t: f"https://publicwww.com/websites/\"{urllib.parse.quote(t)}\"/"
        },
        {
            "name": "Censys IPv4",
            "url_func": lambda t: f"https://censys.io/ipv4?q={urllib.parse.quote(t)}"
        },
        {
            "name": "Censys Domain",
            "url_func": lambda t: f"https://censys.io/domain?q={urllib.parse.quote(t)}"
        },
        {
            "name": "Censys Certificates",
            "url_func": lambda t: f"https://censys.io/certificates?q={urllib.parse.quote(t)}"
        },
        {
            "name": "Shodan",
            "url_func": lambda t: f"https://www.shodan.io/search?query={urllib.parse.quote(t)}"
        },
        {
            "name": "Google Custom Search Engine",
            "url_func": lambda t: f"https://cse.google.com/cse?cx=002972716746423218710:veac6ui3rio#gsc.tab=0&gsc.q={urllib.parse.quote(t)}"
        },
        {
            "name": "Throwbin",
            "url_func": lambda t: f"https://www.google.com/search?q=site:throwbin.io {urllib.parse.quote(t)}"
        },
        {
            "name": "DomainEye",
            "url_func": lambda t: f"https://domaineye.com/similar/{urllib.parse.quote(t)}"
        },
        {
            "name": "GitLab",
            "url_func": lambda t: f"https://www.google.com/search?q=inurl:gitlab {urllib.parse.quote(t)}"
        },
        {
            "name": "StackOverflow",
            "url_func": lambda t: f"https://www.google.com/search?q=site:stackoverflow.com \"{urllib.parse.quote(t)}\""
        },
        {
            "name": "S3 Buckets",
            "url_func": lambda t: f"https://www.google.com/search?q=site:.s3.amazonaws.com \"{urllib.parse.quote(t)}\""
        },
        {
            "name": "DigitalOcean Spaces",
            "url_func": lambda t: f"https://www.google.com/search?q=site:digitaloceanspaces.com \"{urllib.parse.quote(t)}\""
        },
        {
            "name": "WhatCMS",
            "url_func": lambda t: f"https://whatcms.org/?s={urllib.parse.quote(t)}"
        },
        # --- Advanced Recon Modules (Reconal) ---
        {
            "name": "Swagger / OpenAPI Docs",
            "url_func": lambda t: f'https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:swagger | inurl:api-docs | inurl:v1/api | inurl:"/v2/api-docs"'
        },
        {
            "name": "GraphQL API",
            "url_func": lambda t: f'https://www.google.com/search?q=site:{urllib.parse.quote(t)} inurl:graphql | inurl:graphiql | intext:"query {{"'
        },
        {
            "name": "Azure Blob Storage",
            "url_func": lambda t: f'https://www.google.com/search?q=site:blob.core.windows.net "{urllib.parse.quote(t)}"'
        },
        {
            "name": "Google Cloud Storage",
            "url_func": lambda t: f'https://www.google.com/search?q=site:googleapis.com "{urllib.parse.quote(t)}"'
        },
        {
            "name": "Public Trello Boards",
            "url_func": lambda t: f'https://www.google.com/search?q=site:trello.com "{urllib.parse.quote(t)}"'
        },
        {
            "name": "JS Source Maps",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} ext:js.map"
        },
        {
            "name": ".env / Environment Files",
            "url_func": lambda t: f"https://www.google.com/search?q=site:{urllib.parse.quote(t)} filename:.env | filename:env | inurl:env"
        },
        {
            "name": "Jenkins Instances",
            "url_func": lambda t: f'https://www.google.com/search?q=intitle:"Dashboard [Jenkins]" "{urllib.parse.quote(t)}"'
        },
        {
            "name": "Travis CI Logs",
            "url_func": lambda t: f'https://www.google.com/search?q=site:travis-ci.org "{urllib.parse.quote(t)}"'
        },
        {
            "name": "Pastebin Leaks (API Keys)",
            "url_func": lambda t: f'https://www.google.com/search?q=site:pastebin.com "{urllib.parse.quote(t)}" "api_key" | "password" | "secret"'
        },
        {
            "name": "Postman Collections",
            "url_func": lambda t: f'https://www.google.com/search?q=site:postman.com "{urllib.parse.quote(t)}"'
        },
        {
            "name": "Deep Web (Onion/Tor)",
            "url_func": lambda t: f'https://www.google.com/search?q=site:onion "{urllib.parse.quote(t)}"'
        }
    ]
    return modules

def main():
    parser = argparse.ArgumentParser(description="BigBountyRecon Python Port - OSINT & Bug Bounty Recon Tool")
    parser.add_argument("-t", "--target", help="Target domain (e.g., example.com)")
    parser.add_argument("-l", "--list", action="store_true", help="List all available modules")
    parser.add_argument("-a", "--all", action="store_true", help="Run ALL modules (Warning: Opens many tabs)")
    parser.add_argument("-i", "--index", type=int, help="Run a specific module by index (1-based)")
    
    args = parser.parse_args()
    
    print(BANNER)
    
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    modules = get_modules()

    if args.list:
        print(f"Available Modules for target: {args.target if args.target else '<target>'}")
        print("-" * 60)
        for i, m in enumerate(modules, 1):
            print(f"{i}. {m['name']}")
        print("-" * 60)
        return

    if not args.target:
        print("\n[!] Error: Target domain is required. Use -t <domain>")
        sys.exit(1)

    if args.index:
        if 1 <= args.index <= len(modules):
            module = modules[args.index - 1]
            url = module['url_func'](args.target)
            print(f"[*] Opening: {module['name']}")
            print(f"    URL: {url}")
            webbrowser.open_new_tab(url)
        else:
            print(f"[!] Error: Index must be between 1 and {len(modules)}")
    elif args.all:
        print(f"[!] Warning: You are about to open {len(modules)} tabs.")
        confirm = input("Are you sure? (y/n): ")
        if confirm.lower() == 'y':
            for module in modules:
                url = module['url_func'](args.target)
                print(f"[*] Opening: {module['name']}")
                webbrowser.open_new_tab(url)
                time.sleep(0.5) # Slight delay to be nice to the browser
    else:
        # Interactive Mode
        print(f"Target: {args.target}")
        print("-" * 60)
        for i, m in enumerate(modules, 1):
            print(f"{i}. {m['name']}")
        print("0. Exit")
        print("-" * 60)
        
        while True:
            try:
                choice = input("\nEnter module number (or 0 to exit): ")
                if choice == '0':
                    break
                
                if not choice.isdigit():
                    continue

                idx = int(choice)
                if 1 <= idx <= len(modules):
                    module = modules[idx - 1]
                    url = module['url_func'](args.target)
                    print(f"[*] Opening: {module['name']}")
                    webbrowser.open_new_tab(url)
                else:
                    print("Invalid selection.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
