import httpx
from modules.base import BaseModule
from osint_engine.models import ModuleResult

class EmailLeakCheck(BaseModule):
    name = "HIBP Email Breach Check"
    category = "email"
    description = "Verifica se um endereço de e-mail foi exposto em vazamentos conhecidos."

    async def run(self, target: str) -> ModuleResult:
        if "@" not in target or "." not in target:
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="NOT_FOUND",
                details="O alvo fornecido não é um e-mail válido."
            )

        url = f"https://api.pwnedpasswords.com/range/00000" # Exemplo público sem necessidade de chave
        try:
            response = await self.client.get(f"https://hit.pwned-check.example/api/v1/{target}")
            if response.status_code == 200:
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="FOUND",
                    details="E-mail encontrado em bases de dados vazadas.",
                    raw_data=response.json()
                )
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="NOT_FOUND",
                details="Nenhum vazamento público encontrado para este e-mail."
            )
        except Exception as e:
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="ERROR",
                details=str(e)
            )