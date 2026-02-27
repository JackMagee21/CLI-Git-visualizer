import click
from rich.console import Console
from rich.table import Table

from gitviz.core.repo import open_repo, RepoError
from gitviz.core.commits import get_commits
from gitviz.analytics.contributors import get_contributor_stats, contribution_percentage

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


@main.command()
@click.argument("path", default=".")
@click.option("--limit", "-n", default=500, help="Number of commits to analyse.")
def contributors(path, limit):
    """Show contributor breakdown — commits, lines changed, and share."""
    try:
        repo = open_repo(path)
    except RepoError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    commits = get_commits(repo, max_count=limit)

    if not commits:
        console.print("[yellow]No commits found.[/yellow]")
        return

    stats = get_contributor_stats(commits)
    percentages = contribution_percentage(stats)

    table = Table(title=f"Contributors — {repo.working_dir}", show_lines=False)
    table.add_column("Author",   style="green",  no_wrap=True)
    table.add_column("Commits",  style="cyan",   justify="right", no_wrap=True)
    table.add_column("Share",    style="yellow", justify="right", no_wrap=True)
    table.add_column("+",        style="green",  justify="right", no_wrap=True)
    table.add_column("-",        style="red",    justify="right", no_wrap=True)
    table.add_column("Files",    style="dim",    justify="right", no_wrap=True)
    table.add_column("Activity", no_wrap=True)

    max_commits = stats[0].commits if stats else 1

    for c in stats:
        pct = percentages.get(c.email, 0.0)
        bar_len = int((c.commits / max_commits) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)

        table.add_row(
            c.author,
            str(c.commits),
            f"{pct}%",
            str(c.insertions),
            str(c.deletions),
            str(c.files_changed),
            f"[cyan]{bar}[/cyan]",
        )

    console.print(table)
    console.print(f"[dim]Analysed {len(commits)} commits across {len(stats)} contributor(s).[/dim]")