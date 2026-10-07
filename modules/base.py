from abc import ABC, abstractmethod
import httpx
from osint_engine.models import ModuleResult

class BaseModule(ABC):
    name: str = "BaseModule"
    category: str = "general"
    description: str = ""

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    @abstractmethod
    async def run(self, target: str) -> ModuleResult:
        """Executa a coleta de inteligência contra o alvo especificado."""
        pass