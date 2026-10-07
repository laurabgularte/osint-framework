import httpx
from modules.base import BaseModule
from osint_engine.models import ModuleResult

class GitHubCheck(BaseModule):
    name = "GitHub Username Check"
    category = "username"
    description = "Verifica se um nome de usuário existe no GitHub via API REST."

    async def run(self, target: str) -> ModuleResult:
        url = f"https://api.github.com/users/{target}"
        try:
            response = await self.client.get(url)
            if response.status_code == 200:
                data = response.json()
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="FOUND",
                    details=f"Perfil: {data.get('html_url')} | Repos: {data.get('public_repos')}",
                    raw_data=data
                )
            elif response.status_code == 404:
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="NOT_FOUND",
                    details="Usuário não encontrado."
                )
            else:
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="ERROR",
                    details=f"Status HTTP {response.status_code}"
                )
        except Exception as e:
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="ERROR",
                details=str(e)
            )