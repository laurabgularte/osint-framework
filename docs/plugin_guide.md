# Guia de Desenvolvimento de Plugins 🔌

Este guia descreve os passos para criar, testar e integrar novos módulos de coleta (plugins) ao **OSINT Framework Engine**.

---

## 🎯 Conceito Base

Todos os plugins do sistema devem herdar da classe abstrata `BaseModule`, localizada em `modules/base.py`. Graças ao mecanismo de busca automática (`loader.py`), **qualquer novo arquivo `.py` criado na pasta `modules/` que implemente essa classe será automaticamente reconhecido e executado pela CLI.**

---

## 🛠️ Criando um Novo Plugin Passo a Passo

### 1. Escolha a Categoria

Crie seu arquivo na subpasta correspondente dentro de `modules/`:

- `modules/username/` -> Verificação de perfis e contas em redes sociais.
- `modules/dns/` -> Enumeração de subdomínios, registros DNS e IP.
- `modules/metadata/` -> Análise de documentos, imagens e metadados.

_(Se necessário, você pode criar uma nova subpasta dentro de `modules/` para novas categorias)._

### 2. Estrutura do Código

Crie o arquivo `modules/username/exemplo_check.py` com a seguinte estrutura:

```python
import httpx
from modules.base import BaseModule
from osint_engine.models import ModuleResult

class ExemploCheck(BaseModule):
    # Metadados obrigatórios do plugin
    name = "Nome do Seu Módulo"
    category = "username"  # Deve coincidir com a categoria temática
    description = "Breve descrição do que o módulo faz."

    async def run(self, target: str) -> ModuleResult:
        url = f"[https://api.exemplo.com/users/](https://api.exemplo.com/users/){target}"

        try:
            # Utilize o cliente HTTP assíncrono herdado de self.client
            response = await self.client.get(url)

            if response.status_code == 200:
                data = response.json()
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="FOUND",
                    details=f"Perfil encontrado: {data.get('url')}",
                    raw_data=data
                )
            elif response.status_code == 404:
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="NOT_FOUND",
                    details="Perfil não existe."
                )
            else:
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="ERROR",
                    details=f"Código HTTP inesperado: {response.status_code}"
                )

        except httpx.RequestError as e:
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="ERROR",
                details=f"Erro de conexão: {str(e)}"
            )
        except Exception as e:
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="ERROR",
                details=f"Erro de execução: {str(e)}"
            )
```
