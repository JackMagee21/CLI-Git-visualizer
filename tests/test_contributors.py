from gitviz.core.commits import get_commits
from gitviz.analytics.contributors import get_contributor_stats, contribution_percentage


def test_contributor_count(sample_repo):
    commits = get_commits(sample_repo)
    stats = get_contributor_stats(commits)
    assert len(stats) == 1  # all commits are by "Test User"


def test_contributor_commit_count(sample_repo):
    commits = get_commits(sample_repo)
    stats = get_contributor_stats(commits)
    assert stats[0].commits == 3


def test_contributor_name(sample_repo):
    commits = get_commits(sample_repo)
    stats = get_contributor_stats(commits)
    assert stats[0].author == "Test User"


def test_sorted_by_commits_descending(sample_repo):
    commits = get_commits(sample_repo)
    stats = get_contributor_stats(commits)
    counts = [s.commits for s in stats]
    assert counts == sorted(counts, reverse=True)


def test_percentage_sums_to_100(sample_repo):
    commits = get_commits(sample_repo)
    stats = get_contributor_stats(commits)
    percentages = contribution_percentage(stats)
    assert sum(percentages.values()) == 100.0


def test_percentage_empty():
    assert contribution_percentage([]) == {}