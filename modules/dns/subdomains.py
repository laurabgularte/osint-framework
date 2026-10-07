from modules.base import BaseModule
from osint_engine.models import ModuleResult

class CRTShSubdomains(BaseModule):
    name = "crt.sh Subdomain Enumerator"
    category = "dns"
    description = "Busca subdomínios expostos nos logs do crt.sh."

    async def run(self, target: str) -> ModuleResult:
        url = f"https://crt.sh/?q=%.{target}&output=json"
        try:
            response = await self.client.get(url)
            if response.status_code == 200:
                entries = response.json()
                subdomains = set()
                for entry in entries:
                    name_value = entry.get("name_value", "")
                    for sub in name_value.split("\n"):
                        sub = sub.strip()
                        if sub and not sub.startswith("*"):
                            subdomains.add(sub)
                
                sub_list = sorted(list(subdomains))[:5]
                total = len(subdomains)
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="FOUND" if total > 0 else "NOT_FOUND",
                    details=f"Encontrados: {total} | Amostra: {', '.join(sub_list)}",
                    raw_data={"total": total, "subdomains": list(subdomains)}
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