# Arquitetura do OSINT Framework Engine 🏗️

O **OSINT Framework Engine** foi projetado seguindo o padrão de arquitetura `src-layout` para Python, garantindo isolamento de contexto, facilidade de manutenção e um sistema modular extensível por plugins.

---

## 📐 Visão Geral da Arquitetura

A engine opera através de um pipeline desacoplado baseado em eventos assíncronos, onde cada fonte de dados é tratada como um plugin independente.

```
[ Usuário / CLI ]
│
▼
[ CLI Layer (cli.py) ]
│
▼
[ Core Orchestrator (core.py) ] ───► [ Config & Logger ]
│
├──────────────────────────────┐
▼                              ▼
[ Plugin Loader (loader.py) ]   [ Async HTTP Client (http_client.py) ]
│                              │
▼                              ▼
[ Módulos / Plugins (modules/) ] ◄────┘
│  (github_check, reddit_check, subdomains, etc.)
│
▼
[ Validação de Dados (models.py) ] ──► [ ModuleResult ]
│
▼
[ Saída Formatada (Rich Table / JSON) ]
```

## 🧩 Componentes Principais

### 1. Camada de Interface CLI (`src/osint_engine/cli.py`)

- Desenvolvida com **Typer** e **Rich**.
- Responsável pelo parsing dos argumentos de linha de comando (`target`, `--category`).
- Formata a resposta da engine em tabelas coloridas e estruturadas para o terminal.

### 2. Orquestrador Core (`src/osint_engine/core.py`)

- Gerencia o ciclo de vida da varredura.
- Instancia o cliente HTTP assíncrono compartilhado (`httpx.AsyncClient`).
- Dispara a execução simultânea de múltiplos módulos via `asyncio.gather`.

### 3. Carregador Dinâmico de Plugins (`src/osint_engine/loader.py`)

- Utiliza `importlib` e `pkgutil` para inspecionar dinamicamente o pacote `modules/`.
- Descobre automaticamente todas as classes que herdam de `BaseModule` sem necessidade de registro manual ou hardcode.
- Adiciona o diretório raiz do projeto ao `sys.path` dinamicamente para resolução segura de imports.

### 4. Modelo de Dados (`src/osint_engine/models.py`)

- Define a estrutura de saída unificada utilizando **Pydantic**:
  - `module_name`: Nome legível do plugin.
  - `category`: Categoria temática (`username`, `dns`, `metadata`).
  - `target`: Alvo investigado.
  - `status`: Estado do resultado (`FOUND`, `NOT_FOUND`, `ERROR`).
  - `details`: Resumo em texto simples para exibição rápida.
  - `raw_data`: Dicionário contendo a resposta JSON bruta da API/coleta.

---

## 🔄 Fluxo de Execução de uma Consulta

1. O usuário executa `osint-cli scan <alvo>`.
2. O `cli.py` recebe a requisição e invoca o `OSINTEngine`.
3. O `loader.py` varre a pasta `modules/` e carrega todos os módulos disponíveis.
4. O `core.py` filtra os módulos ativos (caso `--category` tenha sido informado).
5. Todas as instâncias de plugins recebem um `httpx.AsyncClient` compartilhado e iniciam a coleta em paralelo.
6. Cada módulo retorna um objeto `ModuleResult`.
7. O `cli.py` renderiza os resultados agregados no terminal.
