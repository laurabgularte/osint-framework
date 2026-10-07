# OSINT Framework 🛡️

Uma engine assíncrona, modular e extensível para inteligência de fontes abertas (OSINT) desenvolvida em Python. O projeto utiliza o padrão de arquitetura `src-layout` e um sistema dinâmico de carregamento de plugins que permite adicionar novos módulos de coleta sem alterar o núcleo da aplicação.

---

## ⚡ Recursos Principais

- **Execução Assíncrona de Alta Performance:** Coleta simultânea em múltiplos serviços usando `asyncio` e `httpx`.
- **Arquitetura Orientada a Plugins:** Descoberta e carregamento automático de módulos na pasta `modules/`.
- **Interface CLI Interativa:** Formatação de dados no terminal com tabelas e cores através do `rich` e `typer`.
- **Tipagem e Validação:** Modelos de dados estruturados com `Pydantic` para garantir consistência nas saídas.
- **Filtragem por Categoria:** Opção para executar apenas módulos específicos (ex: `username`, `dns`, `metadata`).

---

## 📁 Estrutura do Repositório

```text
osint-framework/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
│       ├── ci.yml                 # Pipeline de integração contínua (pytest)
│       └── publish.yml
├── docs/
│   ├── architecture.md            # Documentação de arquitetura
│   └── plugin_guide.md            # Guia para desenvolvimento de novos plugins
├── modules/                       # Módulos de coleta (Plugins)
│   ├── __init__.py
│   ├── base.py                    # Classe base abstrata (BaseModule)
│   ├── dns/
│   │   └── subdomains.py          # Enumeração de subdomínios via crt.sh
│   ├── metadata/
│   │   └── exif_parser.py
│   └── username/
│       ├── github_check.py        # Verificação via API do GitHub
│       └── reddit_check.py        # Verificação no Reddit
├── src/
│   └── osint_engine/              # Código fonte principal da Engine
│       ├── __init__.py
│       ├── cli.py                 # Interface de linha de comando (Typer)
│       ├── config.py              # Leitura de variáveis de ambiente
│       ├── core.py                # Orquestrador assíncrono
│       ├── loader.py              # Carregador dinâmico de plugins
│       ├── models.py              # Esquemas de dados (Pydantic)
│       └── utils/
│           ├── http_client.py     # Cliente HTTP assíncrono com User-Agents
│           ├── logger.py          # Logger estilizado
│           └── proxies.py         # Gerenciador de proxies
├── tests/                         # Suíte de testes automatizados
│   ├── test_core.py
│   └── test_modules/
├── .env.example                   # Modelo de configuração de chaves de API
├── .gitignore
├── pyproject.toml                 # Dependências e entrypoints do pacote
└── README.md
```
