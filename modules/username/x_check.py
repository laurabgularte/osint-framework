from modules.base import BaseModule
from osint_engine.models import ModuleResult

class XUsernameCheck(BaseModule):
    name = "X (Twitter) Username Check"
    category = "username"
    description = "Verifica a existência de uma conta no X (Twitter)."

    async def run(self, target: str) -> ModuleResult:
        url = f"https://x.com/{target}"
        try:
            response = await self.client.get(url)
            if response.status_code == 200 and "UserNotFoundError" not in response.text:
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="FOUND",
                    details=f"Perfil encontrado: {url}"
                )
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="NOT_FOUND",
                details="Usuário não existe ou conta suspensa."
            )
        except Exception as e:
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="ERROR",
                details=str(e)
            )