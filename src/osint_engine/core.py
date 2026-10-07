import asyncio
from typing import List, Optional
from osint_engine.loader import ModuleLoader
from osint_engine.models import ModuleResult
from osint_engine.config import config

class OSINTEngine:
    def __init__(self):
        self.loader = ModuleLoader()

    async def run_scan(self, target: str, category: Optional[str] = None) -> List[ModuleResult]:
        modules = self.loader.get_modules(category=category)
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY)

        async def worker(module_cls):
            async with semaphore:
                try:
                    instance = module_cls()
                    return await instance.run(target)
                except Exception as e:
                    return ModuleResult(
                        module_name=getattr(module_cls, "name", "Unknown"),
                        category=getattr(module_cls, "category", "general"),
                        target=target,
                        status="ERROR",
                        details=f"Falha de execução: {str(e)}"
                    )

        tasks = [worker(mod) for mod in modules]
        results = await asyncio.gather(*tasks)
        return list(results)