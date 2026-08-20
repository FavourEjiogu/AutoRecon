from typing import AsyncGenerator
from autorecon.modules.base import ReconModule
from autorecon.core.executor import CommandExecutor
from autorecon.core.dependencies import check_tool

class NmapModule(ReconModule):
    def __init__(self, target: str, scan_type: str = "fast"):
        super().__init__(target)
        self.scan_type = scan_type
        if scan_type == "fast":
            self.name = "Nmap Fast Scan (Top 100)"
            self.flags = ["-F", "-T4"]
        elif scan_type == "full":
            self.name = "Nmap Full Scan (Services & OS)"
            self.flags = ["-sV", "-O", "-T4"]
        elif scan_type == "web":
            self.name = "Nmap Web Ports Scan"
            self.flags = ["-p", "80,443,8080,8443", "-sV"]
        elif scan_type == "deep":
            self.name = "Nmap Deep Scan (All Ports)"
            self.flags = ["-p-", "-T4", "-sV"]
        else:
            self.name = "Nmap Scan"
            self.flags = ["-T4"]
        
    async def execute(self) -> AsyncGenerator[str, None]:
        if not check_tool("nmap"):
            yield "[!] 'nmap' is not installed or not in PATH."
            return
            
        cmd = ["nmap"] + self.flags + [self.target]
        # Attempt to use sudo if -O or -sS is needed, but we avoid interactive prompt blocking
        # by just running as is. If privileges are insufficient, nmap will say so in output.
        yield f"[*] Running: {' '.join(cmd)}"
        
        async for line in CommandExecutor.run_command_stream(cmd, timeout=300):
            yield line
