from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .core import scan_claude_dir

cli = typer.Typer()
console = Console()


@cli.command()
def scan(
    claude_dir: Path = typer.Option("~/.claude", help="Claude config directory"),
    detail: bool = typer.Option(False, "--detail", "-d", help="Show per-session breakdown"),
) -> None:
    """Analyze token usage across all Claude Code projects."""
    claude_dir = claude_dir.expanduser()
    projects = scan_claude_dir(claude_dir)

    if not projects:
        console.print("[yellow]No session data found[/yellow]")
        return

    table = Table(title="Token Usage by Project")
    table.add_column("Project", style="cyan")
    table.add_column("Sessions", justify="right")
    table.add_column("API Calls", justify="right")
    table.add_column("Input", justify="right")
    table.add_column("Output", justify="right")
    table.add_column("Cache Read", justify="right")

    grand_total = 0
    for p in projects:
        table.add_row(
            p.path,
            str(len(p.sessions)),
            str(p.total_api_calls),
            f"{p.total_input:,}",
            f"{p.total_output:,}",
            f"{p.total_cache_read:,}",
        )
        grand_total += p.total_input + p.total_output

    console.print(table)
    console.print(f"\nTotal tokens across all projects: [bold]{grand_total:,}[/bold]")

    if detail:
        console.print()
        for p in projects:
            stable = Table(title=f"Sessions: {p.path}")
            stable.add_column("Session ID", style="cyan")
            stable.add_column("Model")
            stable.add_column("Calls", justify="right")
            stable.add_column("Input", justify="right")
            stable.add_column("Output", justify="right")
            for s in sorted(p.sessions, key=lambda x: -x.input_tokens):
                stable.add_row(
                    s.session_id[:16],
                    s.model,
                    str(s.api_calls),
                    f"{s.input_tokens:,}",
                    f"{s.output_tokens:,}",
                )
            console.print(stable)


def main() -> None:
    cli()
