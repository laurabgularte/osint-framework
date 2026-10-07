import asyncio
import json
import csv
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from osint_engine.core import OSINTEngine
from osint_engine.models import ModuleResult

app = typer.Typer(
    help="OSINT Framework - CLI Tool",
    no_args_is_help=True
)

@app.callback()
def main():
    """OSINT Framework CLI Engine"""
    pass

def save_report(results: list[ModuleResult], file_path: Path):
    """Guarda os resultados num ficheiro JSON ou CSV consoante a extensão."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    data = [res.model_dump() for res in results]

    if file_path.suffix.lower() == ".json":
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    elif file_path.suffix.lower() == ".csv":
        if not data:
            return
        fieldnames = list(data[0].keys())
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

@app.command(name="scan")
def scan(
    target: str = typer.Argument(..., help="Alvo para investigação (username, domínio ou e-mail)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filtrar por categoria (ex: username, dns, email)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Caminho do ficheiro para salvar o relatório (.json ou .csv)"),
    json_output: bool = typer.Option(False, "--json", help="Exibir apenas JSON bruto no stdout")
):
    """Executa varredura OSINT assíncrona contra o alvo especificado."""
    console = Console()
    
    if not json_output:
        console.print("\n[bold magenta]=== OSINT Framework Engine ===[/bold magenta]")
        console.print(f"[bold blue][*] Alvo:[/bold blue] {target}")
        if category:
            console.print(f"[bold blue][*] Categoria:[/bold blue] {category}")
        console.print("[dim]Carregando módulos e iniciando varredura...[/dim]\n")

    engine = OSINTEngine()
    results = asyncio.run(engine.run_scan(target, category=category))

    if json_output:
        raw_json = json.dumps([res.model_dump() for res in results], indent=2, ensure_ascii=False)
        print(raw_json)
        return

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

    if output:
        save_report(results, output)
        console.print(f"\n[bold green][+] Relatório salvo com sucesso em:[/bold green] {output}")

if __name__ == "__main__":
    app()