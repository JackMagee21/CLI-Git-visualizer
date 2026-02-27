from gitviz.core.commits import get_commits


def test_get_commits_returns_all(sample_repo):
    commits = get_commits(sample_repo)
    assert len(commits) == 3


def test_get_commits_respects_limit(sample_repo):
    commits = get_commits(sample_repo, max_count=2)
    assert len(commits) == 2


def test_commit_fields_are_populated(sample_repo):
    commits = get_commits(sample_repo)
    latest = commits[0]  # most recent first

    assert latest.sha  == latest.sha[:7]  # truncated to 7 chars
    assert latest.author == "Test User"
    assert latest.email == "test@example.com"
    assert latest.message == "Add utils module"
    assert latest.date is not None


def test_commit_sha_is_7_chars(sample_repo):
    commits = get_commits(sample_repo)
    for c in commits:
        assert len(c.sha) == 7


def test_commit_messages_are_first_line_only(sample_repo):
    commits = get_commits(sample_repo)
    for c in commits:
        assert "\n" not in c.message