#!/usr/bin/env python3
import sys
import os

# Add local path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autorecon.ui.tui_app import AutoReconApp
from autorecon.core.dependencies import check_all_dependencies, get_install_command
import subprocess

def check_env():
    status, missing = check_all_dependencies()
    if missing:
        print(f"[!] Warning: The following tools are missing: {', '.join(missing)}")
        choice = input("[?] Would you like to auto-install them using sudo apt? (y/n): ").strip().lower()
        if choice == 'y':
            print("[*] Running sudo apt-get update...")
            subprocess.run(["sudo", "apt-get", "update"])
            cmd = get_install_command(missing)
            print(f"[*] Running: {cmd}")
            subprocess.run(cmd.split())
            print("[+] Environment successfully provisioned!")
            input("\nPress Enter to launch the TUI...")
        else:
            print("[!] Some modules might fail or use fallbacks.")
            input("\nPress Enter to proceed anyway...")

if __name__ == "__main__":
    check_env()
    app = AutoReconApp()
    app.run()
