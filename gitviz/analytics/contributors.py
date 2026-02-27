from dataclasses import dataclass, field
from collections import defaultdict
from gitviz.core.commits import CommitInfo


@dataclass
class ContributorStats:
    author: str
    email: str
    commits: int = 0
    insertions: int = 0
    deletions: int = 0
    files_changed: int = 0

    @property
    def total_changes(self) -> int:
        return self.insertions + self.deletions


def get_contributor_stats(commits: list[CommitInfo]) -> list[ContributorStats]:
    """Aggregate commit data by author, sorted by commit count descending."""
    authors: dict[str, ContributorStats] = {}

    for commit in commits:
        key = commit.email  # use email as unique key (names can vary)

        if key not in authors:
            authors[key] = ContributorStats(author=commit.author, email=commit.email)

        authors[key].commits += 1
        authors[key].insertions += commit.insertions
        authors[key].deletions += commit.deletions
        authors[key].files_changed += commit.files_changed

    return sorted(authors.values(), key=lambda c: c.commits, reverse=True)


def contribution_percentage(stats: list[ContributorStats]) -> dict[str, float]:
    """Returns each author's share of total commits as a percentage."""
    total = sum(c.commits for c in stats)
    if total == 0:
        return {}
    return {c.email: round((c.commits / total) * 100, 1) for c in stats}