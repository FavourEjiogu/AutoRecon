from typing import AsyncGenerator
from autorecon.modules.base import ReconModule
from autorecon.core.executor import CommandExecutor
from autorecon.core.dependencies import check_tool

class NiktoModule(ReconModule):
    def __init__(self, target: str):
        super().__init__(target)
        self.name = "Nikto Web Audit"
        
    async def execute(self) -> AsyncGenerator[str, None]:
        if not check_tool("nikto"):
            yield "[!] 'nikto' is not installed or not in PATH."
            return
            
        cmd = ["nikto", "-h", self.target, "-Tuning", "123", "-maxtime", "5m"]
        yield f"[*] Running: {' '.join(cmd)}"
        
        async for line in CommandExecutor.run_command_stream(cmd, timeout=360):
            yield line
