import os

APP_NAME = "AutoRecon Studio"
APP_VERSION = "1.0.0"

# Directories
# __file__ is autorecon/core/config.py, so we go up 3 levels to get to AutoRecon/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, "reports")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Tool Definitions
TOOLS = {
    "ping": "iputils-ping",
    "whois": "whois",
    "dig": "dnsutils",
    "nmap": "nmap",
    "subfinder": "subfinder",
    "nikto": "nikto"
}

# Scan Presets
PRESETS = {
    "quick_passive": {
        "name": "Quick Passive",
        "description": "WHOIS + DNS Dig + Certificate Transparency (No packets sent to target)",
        "modules": ["whois", "dns", "subdomain"]
    },
    "host_verification": {
        "name": "Host Verification",
        "description": "Ping + Fast Top 100 Port Scan",
        "modules": ["ping", "nmap_fast"]
    },
    "full_surface_audit": {
        "name": "Full Surface Audit",
        "description": "Passive OSINT + Full Nmap Scan + Nikto Web Audit",
        "modules": ["whois", "dns", "subdomain", "ping", "nmap_full", "nikto"]
    },
    "web_discovery": {
        "name": "Web Discovery",
        "description": "Subdomain Enumeration + Nikto + HTTP/HTTPS Nmap Scan",
        "modules": ["subdomain", "nmap_web", "nikto"]
    },
    "deep_port_scan": {
        "name": "Deep Port Scan",
        "description": "Nmap scan on all 65535 ports with SYN stealth",
        "modules": ["nmap_deep"]
    },
    "dns_only": {
        "name": "DNS & Subdomain Only",
        "description": "DNS queries and subdomain enumeration",
        "modules": ["dns", "subdomain"]
    },
    "custom": {
        "name": "Custom Mode",
        "description": "Select individual modules for tailored reconnaissance",
        "modules": [] # Filled dynamically in UI
    }
}
