from typing import AsyncGenerator
from autorecon.modules.base import ReconModule
from autorecon.core.executor import CommandExecutor
from autorecon.core.dependencies import check_tool

class PingModule(ReconModule):
    def __init__(self, target: str):
        super().__init__(target)
        self.name = "Ping (ICMP Reachability)"
        
    async def execute(self) -> AsyncGenerator[str, None]:
        if not check_tool("ping"):
            yield "[!] 'ping' is not installed or not in PATH."
            return
            
        cmd = ["ping", "-c", "4", self.target]
        yield f"[*] Running: {' '.join(cmd)}"
        
        async for line in CommandExecutor.run_command_stream(cmd, timeout=30):
            yield line
