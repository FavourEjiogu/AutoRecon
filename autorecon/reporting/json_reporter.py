import json
import os
import datetime
from autorecon.core.config import OUTPUT_DIR

def generate_json_report(target: str, results: dict, duration: int) -> str:
    """Generates a JSON report and saves it to the output directory."""
    timestamp = datetime.datetime.now().isoformat()
    
    report_data = {
        "target": target,
        "timestamp": timestamp,
        "duration_seconds": duration,
        "results": results
    }
    
    safe_target = target.replace(".", "_").replace(":", "_").replace("/", "_")
    filename = f"autorecon_{safe_target}_{int(datetime.datetime.now().timestamp())}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
        
    return filepath
