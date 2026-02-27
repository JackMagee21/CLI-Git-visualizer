from pathlib import Path
import git


class RepoError(Exception):
    pass


def open_repo(path: str) -> git.Repo:
    """Open a Git repository at the given path."""
    resolved = Path(path).resolve()

    if not resolved.exists():
        raise RepoError(f"Path does not exist: {resolved}")

    try:
        repo = git.Repo(resolved, search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        raise RepoError(f"No Git repository found at: {resolved}")
    except git.NoSuchPathError:
        raise RepoError(f"Path not found: {resolved}")

    return repo