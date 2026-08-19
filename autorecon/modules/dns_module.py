from typing import AsyncGenerator
from autorecon.modules.base import ReconModule
from autorecon.core.executor import CommandExecutor
from autorecon.core.dependencies import check_tool

class DnsModule(ReconModule):
    def __init__(self, target: str):
        super().__init__(target)
        self.name = "DNS Enumeration"
        
    async def execute(self) -> AsyncGenerator[str, None]:
        if not check_tool("dig"):
            yield "[!] 'dig' is not installed or not in PATH."
            return
            
        cmd = ["dig", self.target, "ANY", "+short"]
        yield f"[*] Running: {' '.join(cmd)}"
        
        async for line in CommandExecutor.run_command_stream(cmd, timeout=30):
            yield line
        
        yield ""
        cmd_full = ["dig", self.target, "ANY", "+noall", "+answer"]
        yield f"[*] Running: {' '.join(cmd_full)}"
        
        async for line in CommandExecutor.run_command_stream(cmd_full, timeout=30):
            yield line
