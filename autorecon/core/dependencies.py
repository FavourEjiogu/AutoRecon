import shutil
from typing import Dict, Tuple

from autorecon.core.config import TOOLS

def check_tool(tool_name: str) -> bool:
    """Checks if a tool exists in the system PATH"""
    return shutil.which(tool_name) is not None

def check_all_dependencies() -> Tuple[Dict[str, bool], list]:
    """
    Checks all tools defined in config.
    Returns:
        tuple: (dict of tool_name -> bool, list of missing tools)
    """
    status = {}
    missing = []
    
    for tool in TOOLS:
        is_installed = check_tool(tool)
        status[tool] = is_installed
        if not is_installed:
            missing.append(tool)
            
    return status, missing

def get_install_command(missing_tools: list) -> str:
    """Generates an apt install command for missing tools."""
    packages = []
    for tool in missing_tools:
        if tool in TOOLS:
            packages.append(TOOLS[tool])
    
    if packages:
        return f"sudo apt-get install -y {' '.join(packages)}"
    return ""
