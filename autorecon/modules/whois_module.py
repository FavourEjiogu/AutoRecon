from typing import AsyncGenerator
from autorecon.modules.base import ReconModule
from autorecon.core.executor import CommandExecutor
from autorecon.core.dependencies import check_tool

class WhoisModule(ReconModule):
    def __init__(self, target: str):
        super().__init__(target)
        self.name = "WHOIS Lookup"
        
    async def execute(self) -> AsyncGenerator[str, None]:
        if not check_tool("whois"):
            yield "[!] 'whois' is not installed or not in PATH."
            return
            
        cmd = ["whois", self.target]
        yield f"[*] Running: {' '.join(cmd)}"
        
        async for line in CommandExecutor.run_command_stream(cmd, timeout=30):
            yield line
