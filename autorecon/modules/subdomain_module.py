import json
import urllib.request
import urllib.error
from typing import AsyncGenerator
from autorecon.modules.base import ReconModule
from autorecon.core.executor import CommandExecutor
from autorecon.core.dependencies import check_tool

class SubdomainModule(ReconModule):
    def __init__(self, target: str):
        super().__init__(target)
        self.name = "Subdomain Enumeration"
        
    async def execute(self) -> AsyncGenerator[str, None]:
        if check_tool("subfinder"):
            cmd = ["subfinder", "-d", self.target, "-silent"]
            yield f"[*] Running: {' '.join(cmd)}"
            async for line in CommandExecutor.run_command_stream(cmd, timeout=120):
                yield line
        else:
            yield "[!] 'subfinder' is not installed. Falling back to crt.sh query..."
            try:
                url = f"https://crt.sh/?q=%25.{self.target}&output=json"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode())
                    subdomains = set()
                    for entry in data:
                        name = entry.get('name_value', '')
                        if name:
                            for sub in name.split('\n'):
                                sub = sub.strip()
                                if sub.endswith(self.target):
                                    subdomains.add(sub)
                    for sub in sorted(list(subdomains)):
                        yield sub
            except urllib.error.URLError as e:
                yield f"[-] crt.sh query failed: {e}"
            except Exception as e:
                yield f"[-] Error processing crt.sh data: {e}"
