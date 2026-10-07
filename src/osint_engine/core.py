import asyncio
from typing import List, Optional
from osint_engine.loader import load_plugins
from osint_engine.models import ModuleResult
from osint_engine.utils.http_client import create_async_client

class OSINTEngine:
    def __init__(self):
        self.plugin_classes = load_plugins("modules")

    async def run_scan(self, target: str, category: Optional[str] = None) -> List[ModuleResult]:
        async with create_async_client() as client:
            tasks = []
            for cls in self.plugin_classes:
                instance = cls(http_client=client)
                if category and instance.category.lower() != category.lower():
                    continue
                tasks.append(instance.run(target))

            if not tasks:
                return []

            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [res for res in results if isinstance(res, ModuleResult)]