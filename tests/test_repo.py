import pytest
from pathlib import Path

import git

from gitviz.core.repo import open_repo, RepoError


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------


def test_open_repo_returns_repo_instance(sample_repo, tmp_path):
    """Opening a valid Git repository returns a git.Repo object."""
    # sample_repo.working_dir is the root of the temp repo
    repo = open_repo(str(sample_repo.working_dir))
    assert isinstance(repo, git.Repo)


def test_open_repo_accepts_subdirectory(sample_repo):
    """open_repo walks up to the repository root when given a subdirectory."""
    subdir = Path(sample_repo.working_dir) / "subdir"
    subdir.mkdir()

    repo = open_repo(str(subdir))
    assert isinstance(repo, git.Repo)
    # The resolved working_dir should be the repo root, not the subdirectory
    assert Path(repo.working_dir).resolve() == Path(sample_repo.working_dir).resolve()


def test_open_repo_default_dot_inside_repo(sample_repo, monkeypatch):
    """open_repo(".") resolves relative to the current working directory."""
    monkeypatch.chdir(sample_repo.working_dir)
    repo = open_repo(".")
    assert isinstance(repo, git.Repo)


def test_open_repo_working_dir_is_populated(sample_repo):
    """The returned Repo object has a working_dir attribute set."""
    repo = open_repo(str(sample_repo.working_dir))
    assert repo.working_dir is not None
    assert Path(repo.working_dir).exists()


# ---------------------------------------------------------------------------
# Error-path tests
# ---------------------------------------------------------------------------


def test_open_repo_nonexistent_path_raises_repo_error():
    """A path that does not exist on disk raises RepoError."""
    with pytest.raises(RepoError, match="does not exist"):
        open_repo("/this/path/absolutely/does/not/exist/anywhere")


def test_open_repo_non_git_directory_raises_repo_error(tmp_path):
    """A directory that exists but is not a Git repository raises RepoError."""
    with pytest.raises(RepoError, match="No Git repository found"):
        open_repo(str(tmp_path))


def test_open_repo_file_path_raises_repo_error(tmp_path):
    """Passing a path that points to a file (not a directory) raises RepoError.

    git.Repo will either raise InvalidGitRepositoryError or NoSuchPathError
    depending on the gitpython version; both should surface as RepoError.
    """
    file_path = tmp_path / "not_a_repo.txt"
    file_path.write_text("hello")

    with pytest.raises(RepoError):
        open_repo(str(file_path))


# ---------------------------------------------------------------------------
# RepoError contract tests
# ---------------------------------------------------------------------------


def test_repo_error_is_exception():
    """RepoError must be a proper Exception subclass so callers can catch it."""
    err = RepoError("something went wrong")
    assert isinstance(err, Exception)
    assert str(err) == "something went wrong"


def test_repo_error_message_contains_path():
    """Error messages should include the offending path for debuggability."""
    bad_path = "/nonexistent/repo"
    with pytest.raises(RepoError) as exc_info:
        open_repo(bad_path)
    # The error message should mention the path so users know what failed
    assert bad_path in str(exc_info.value) or "nonexistent" in str(exc_info.value)