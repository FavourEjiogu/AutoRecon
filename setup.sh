#!/bin/bash

set -e

echo "[*] Setting up AutoRecon Studio Environment..."

# Note: System packages like nmap, subfinder, nikto, whois, dnsutils
# should be installed by the user manually if missing via:
# sudo apt-get install -y python3-venv python3-pip iputils-ping whois dnsutils nmap subfinder nikto

# Create Python virtual environment
if [ ! -d ".venv" ]; then
    echo "[*] Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate venv and install python dependencies
echo "[*] Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Setup complete! Run the application using:"
echo "    source .venv/bin/activate"
echo "    python3 app.py"
