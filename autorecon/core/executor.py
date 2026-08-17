import asyncio
import os
from typing import AsyncGenerator, Dict

class CommandExecutor:
    @staticmethod
    async def run_command_stream(cmd: list, timeout: int = 300) -> AsyncGenerator[str, None]:
        """
        Runs a command asynchronously and yields stdout/stderr lines as they arrive.
        """
        process = None
        try:
            # We use a combined stderr to stdout pipe so we get all output in order
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )

            async def read_stream(stream):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    yield line.decode('utf-8', errors='replace').rstrip('\n')

            # Wait for output with a timeout
            async def consume_output():
                async for line in read_stream(process.stdout):
                    yield line

            async_gen = consume_output()
            
            while True:
                try:
                    line = await asyncio.wait_for(async_gen.__anext__(), timeout=timeout)
                    yield line
                except StopAsyncIteration:
                    break
                    
            await process.wait()

        except asyncio.TimeoutError:
            if process and process.returncode is None:
                process.terminate()
            yield f"[!] Command timed out after {timeout} seconds."
        except Exception as e:
            yield f"[!] Executor Error: {str(e)}"
        finally:
            if process and process.returncode is None:
                try:
                    process.terminate()
                except ProcessLookupError:
                    pass

    @staticmethod
    async def run_command_sync(cmd: list, timeout: int = 300) -> Dict:
        """
        Runs a command and waits for it to complete, returning all output.
        """
        output = []
        async for line in CommandExecutor.run_command_stream(cmd, timeout):
            output.append(line)
        return {
            "output": "\n".join(output),
            "lines": output
        }
