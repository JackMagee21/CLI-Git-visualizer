from dataclasses import dataclass
from datetime import datetime
import git


@dataclass
class CommitInfo:
    sha: str
    author: str
    email: str
    message: str
    date: datetime
    files_changed: int
    insertions: int
    deletions: int


def get_commits(repo: git.Repo, max_count: int = 100) -> list[CommitInfo]:
    """Extract commit data from a repository."""
    commits = []

    for commit in repo.iter_commits(max_count=max_count):
        # stats can be slow for large repos, but fine for now
        stats = commit.stats.total

        commits.append(CommitInfo(
            sha=commit.hexsha[:7],
            author=commit.author.name,
            email=commit.author.email,
            message=commit.message.strip().splitlines()[0],  # first line only
            date=datetime.fromtimestamp(commit.committed_date),
            files_changed=stats.get("files", 0),
            insertions=stats.get("insertions", 0),
            deletions=stats.get("deletions", 0),
        ))

    return commits