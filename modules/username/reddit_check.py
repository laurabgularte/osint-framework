from modules.base import BaseModule
from osint_engine.models import ModuleResult

class RedditCheck(BaseModule):
    name = "Reddit Username Check"
    category = "username"
    description = "Verifica a existência de um perfil no Reddit."

    async def run(self, target: str) -> ModuleResult:
        url = f"https://www.reddit.com/user/{target}/about.json"
        try:
            response = await self.client.get(url)
            if response.status_code == 200:
                data = response.json().get("data", {})
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="FOUND",
                    details=f"Perfil: https://reddit.com/user/{target} | Karma: {data.get('total_karma', 0)}",
                    raw_data=data
                )
            elif response.status_code in (404, 403):
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="NOT_FOUND",
                    details="Usuário não existe ou está suspenso."
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