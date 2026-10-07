import asyncio
import typer
from rich.console import Console
from rich.table import Table
from osint_engine.core import OSINTEngine

app = typer.Typer(
    help="OSINT Framework - CLI Tool",
    no_args_is_help=True
)

@app.callback()
def main():
    """
    OSINT Framework CLI Engine
    """
    pass

@app.command(name="scan")
def scan(
    target: str = typer.Argument(..., help="Alvo para investigação (username ou domínio)"),
    category: str = typer.Option(None, "--category", "-c", help="Filtrar por categoria (ex: username, dns)")
):
    """Executa varredura OSINT assíncrona contra o alvo especificado."""
    console = Console()
    console.print("\n[bold magenta]=== OSINT Framework Engine ===[/bold magenta]")
    console.print(f"[bold blue][*] Alvo:[/bold blue] {target}")
    if category:
        console.print(f"[bold blue][*] Categoria:[/bold blue] {category}")
    console.print("[dim]Carregando módulos e iniciando varredura...[/dim]\n")

    engine = OSINTEngine()
    results = asyncio.run(engine.run_scan(target, category=category))

    if not results:
        console.print("[yellow]Nenhum módulo executado.[/yellow]")
        return

    table = Table(title=f"Resultados para {target}")
    table.add_column("Módulo", style="cyan", no_wrap=True)
    table.add_column("Categoria", style="yellow")
    table.add_column("Status", style="bold")
    table.add_column("Detalhes", style="white")

    for res in results:
        status_color = "green" if res.status == "FOUND" else ("red" if res.status == "ERROR" else "dim")
        table.add_row(
            res.module_name,
            res.category,
            f"[{status_color}]{res.status}[/{status_color}]",
            res.details or ""
        )

    console.print(table)

if __name__ == "__main__":
    app()