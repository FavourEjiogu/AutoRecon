#!/usr/bin/env python3
import sys
import os
import argparse
import asyncio
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autorecon.core.config import PRESETS
from autorecon.core.validator import validate_target
from autorecon.ui.tui_app import AutoReconApp
from autorecon.reporting.html_reporter import generate_html_report
from autorecon.reporting.json_reporter import generate_json_report

async def run_cli(target: str, profile_id: str):
    validation = validate_target(target)
    if not validation["valid"]:
        print(f"[!] Invalid target: {validation['error']}")
        sys.exit(1)
        
    if profile_id not in PRESETS:
        print(f"[!] Invalid profile. Available: {', '.join(PRESETS.keys())}")
        sys.exit(1)
        
    target = validation["target"]
    profile = PRESETS[profile_id]
    print(f"[*] Starting AutoRecon CLI against {target} with profile {profile['name']}")
    
    app = AutoReconApp()
    results = {}
    start_time = time.time()
    
    for mod_key in profile["modules"]:
        module = app.get_module_instance(mod_key, target)
        if not module:
            continue
            
        print(f"\n[*] Running: {module.name}")
        module_output = []
        async for line in module.execute():
            print(line)
            module_output.append(line)
        results[module.name] = "\n".join(module_output)
        
    duration = int(time.time() - start_time)
    print("\n[*] Generating reports...")
    
    html_path = generate_html_report(target, results, duration)
    json_path = generate_json_report(target, results, duration)
    
    print(f"[+] HTML Report: {html_path}")
    print(f"[+] JSON Report: {json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoRecon CLI")
    parser.add_argument("-t", "--target", required=True, help="Target IP or Domain")
    parser.add_argument("-p", "--profile", required=True, choices=PRESETS.keys(), help="Scan profile to run")
    
    args = parser.parse_args()
    asyncio.run(run_cli(args.target, args.profile))
