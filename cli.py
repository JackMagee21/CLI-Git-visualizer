import click
from rich.console import Console
from rich.table import Table

from gitviz.core.repo import open_repo, RepoError
from gitviz.core.commits import get_commits

console = Console()


@click.group()
def main():
    """Git Visualizer - analyze and visualize your Git history."""
    pass


@main.command()
@click.argument("path", default=".")
@click.option("--limit", "-n", default=20, help="Number of commits to show.")
def log(path, limit):
    """Show recent commits in a formatted table."""
    try:
        repo = open_repo(path)
    except RepoError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    commits = get_commits(repo, max_count=limit)

    if not commits:
        console.print("[yellow]No commits found.[/yellow]")
        return

    table = Table(title=f"Recent Commits — {repo.working_dir}", show_lines=False)
    table.add_column("SHA",     style="cyan",  no_wrap=True)
    table.add_column("Date",    style="dim",   no_wrap=True)
    table.add_column("Author",  style="green", no_wrap=True)
    table.add_column("Message", style="white")
    table.add_column("+",       style="green", justify="right", no_wrap=True)
    table.add_column("-",       style="red",   justify="right", no_wrap=True)

    for c in commits:
        table.add_row(
            c.sha,
            c.date.strftime("%Y-%m-%d"),
            c.author,
            c.message,
            str(c.insertions),
            str(c.deletions),
        )

    console.print(table)