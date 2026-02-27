import pytest
import git
from pathlib import Path


@pytest.fixture
def sample_repo(tmp_path: Path) -> git.Repo:
    """Creates a temporary Git repo with a few commits for testing."""
    repo = git.Repo.init(tmp_path)

    # Required for git to work in CI / clean environments
    repo.config_writer().set_value("user", "name", "Test User").release()
    repo.config_writer().set_value("user", "email", "test@example.com").release()

    # Commit 1
    file1 = tmp_path / "hello.py"
    file1.write_text("print('hello')\n")
    repo.index.add(["hello.py"])
    repo.index.commit("Initial commit")

    # Commit 2
    file1.write_text("print('hello world')\n")
    repo.index.add(["hello.py"])
    repo.index.commit("Update hello message")

    # Commit 3 - add a second file
    file2 = tmp_path / "utils.py"
    file2.write_text("def add(a, b):\n    return a + b\n")
    repo.index.add(["utils.py"])
    repo.index.commit("Add utils module")

    return repo