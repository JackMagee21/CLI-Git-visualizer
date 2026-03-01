import pytest
from gitviz.core.commits import get_commits
from gitviz.analytics.stats import get_repo_stats


def test_total_commits(sample_repo):
    commits = get_commits(sample_repo)
    s = get_repo_stats(commits)
    assert s.total_commits == 3


def test_total_authors(sample_repo):
    commits = get_commits(sample_repo)
    s = get_repo_stats(commits)
    assert s.total_authors == 1


def test_most_active_author(sample_repo):
    commits = get_commits(sample_repo)
    s = get_repo_stats(commits)
    assert s.most_active_author == "Test User"


def test_first_and_latest_commit_order(sample_repo):
    commits = get_commits(sample_repo)
    s = get_repo_stats(commits)
    assert s.first_commit <= s.latest_commit


def test_insertions_and_deletions_are_non_negative(sample_repo):
    commits = get_commits(sample_repo)
    s = get_repo_stats(commits)
    assert s.total_insertions >= 0
    assert s.total_deletions >= 0


def test_empty_commits_raises():
    with pytest.raises(ValueError, match="No commits"):
        get_repo_stats([])