from abc import ABC, abstractmethod
from typing import AsyncGenerator

class ReconModule(ABC):
    def __init__(self, target: str):
        self.target = target
        self.name = self.__class__.__name__

    @abstractmethod
    async def execute(self) -> AsyncGenerator[str, None]:
        """
        Executes the module, yielding output lines as they become available.
        Must be implemented by all subclasses.
        """
        pass
