# gitviz

A fast, zero-config CLI for exploring Git repository history in your terminal.
Understand who is contributing, what is changing, and how active your repository is — without leaving the command line.

```
$ gitviz contributors .

 Contributors — /home/user/my-project
┌───────────────┬─────────┬───────┬───────┬──────┬───────┬──────────────────────┐
│ Author        │ Commits │ Share │     + │    - │ Files │ Activity             │
├───────────────┼─────────┼───────┼───────┼──────┼───────┼──────────────────────┤
│ Alice Chen    │      87 │ 52.1% │ 14203 │ 3812 │   201 │ ████████████████░░░░ │
│ Bob Martínez  │      56 │ 33.5% │  9411 │ 2100 │   134 │ ████████████░░░░░░░░ │
│ Carol Osei    │      24 │ 14.4% │  3204 │  890 │    67 │ █████░░░░░░░░░░░░░░░ │
└───────────────┴─────────┴───────┴───────┴──────┴───────┴──────────────────────┘
Analysed 167 commits across 3 contributor(s).
```

---

## Features

- **`log`** — formatted commit table with author, date, message, and diff stats
- **`contributors`** — per-author breakdown with commit share and inline activity bar
- **`stats`** — high-level repository health summary (total commits, authors, busiest day, top author, commits/day)
- Pure terminal output via [Rich](https://github.com/Textualize/rich) — no browser, no server, no config files
- Works on any local Git repository

---

## Requirements

- Python ≥ 3.10
- Git installed and available on `PATH`

---

## Installation

### Recommended — editable install (development)

```bash
git clone https://github.com/your-org/gitviz.git
cd gitviz
pip install -e .
```

This installs the `gitviz` entry point globally in your current Python environment so you can call it from any directory.

### From source (non-editable)

```bash
pip install .
```

### Dependencies

| Package | Purpose |
|---|---|
| [gitpython](https://gitpython.readthedocs.io) | Reading Git repository data |
| [click](https://click.palletsprojects.com) | CLI argument parsing |
| [rich](https://github.com/Textualize/rich) | Terminal tables, panels, and colour |

---

## Usage

All commands accept a `PATH` argument (defaults to `.`, the current directory). `gitviz` will walk up parent directories to find the repository root, so you can run it from any subdirectory inside a repo.

### `log` — recent commit history

```bash
gitviz log [PATH] [--limit N]
```

Shows the most recent commits in a colour-coded table.

| Column | Description |
|---|---|
| SHA | Abbreviated 7-character commit hash |
| Date | Commit date (YYYY-MM-DD) |
| Author | Commit author name |
| Message | First line of the commit message |
| + | Lines inserted |
| - | Lines deleted |

**Options**

| Flag | Default | Description |
|---|---|---|
| `--limit` / `-n` | `20` | Maximum number of commits to display |

**Example**

```bash
gitviz log ~/projects/my-api -n 50
```

---

### `contributors` — author breakdown

```bash
gitviz contributors [PATH] [--limit N]
```

Aggregates commit history by author, sorted by commit count descending.

| Column | Description |
|---|---|
| Author | Contributor display name |
| Commits | Total commits attributed to this author |
| Share | Percentage of total commits |
| + | Total lines inserted across all commits |
| - | Total lines deleted across all commits |
| Files | Cumulative files changed |
| Activity | Proportional bar chart relative to the top contributor |

> **Note:** Authors are deduplicated by email address, so name changes across commits are handled correctly.

**Options**

| Flag | Default | Description |
|---|---|---|
| `--limit` / `-n` | `500` | Number of commits to analyse |

**Example**

```bash
gitviz contributors . -n 1000
```

---

### `stats` — repository summary

```bash
gitviz stats [PATH] [--limit N]
```

Displays a panel grid of high-level repository metrics.

| Metric | Description |
|---|---|
| Commits | Total commits analysed |
| Authors | Distinct author count (by email) |
| Insertions | Total lines inserted |
| Deletions | Total lines deleted |
| Most Active Day | Day of the week with the most commits |
| Top Author | Author with the most commits |
| Commits/Day | Average daily commit rate over the repo's lifetime |
| First Commit | Date of the earliest commit in the analysed window |
| Latest Commit | Date of the most recent commit |

**Options**

| Flag | Default | Description |
|---|---|---|
| `--limit` / `-n` | `500` | Number of commits to analyse |

**Example**

```bash
gitviz stats /path/to/repo
```

---

## Project Structure

```
gitviz/
├── cli.py                        # Click entry point; all command definitions
├── core/
│   ├── repo.py                   # Repository discovery and error handling
│   └── commits.py                # Raw commit extraction from gitpython
└── analytics/
    ├── contributors.py           # Per-author aggregation and percentage share
    └── stats.py                  # High-level repository statistics

tests/
├── conftest.py                   # Shared pytest fixtures (in-memory git repo)
├── test_commits.py               # Unit tests for commit extraction
├── test_contributors.py          # Unit tests for contributor analytics
├── test_repo.py                  # Unit tests for repository discovery
└── test_stats.py                 # Unit tests for repository statistics
```

### Layer responsibilities

```
CLI (cli.py)
  └── calls Core to open the repo and fetch commits
        └── calls Analytics to compute derived statistics
              └── returns plain dataclasses back up to CLI for rendering
```

The CLI layer owns all Rich formatting. The analytics and core layers are pure Python — no I/O, no terminal dependencies — which keeps them easy to test and reuse.

---

## Development

### Running tests

```bash
pip install -e ".[dev]"   # if you add a dev extra; otherwise:
pip install pytest
pytest
```

Tests use a fully in-memory temporary Git repository created by the `sample_repo` fixture in `conftest.py`. No network access or real repositories are required.

### Running a specific test module

```bash
pytest tests/test_contributors.py -v
```

### Linting and formatting (recommended additions)

```bash
pip install ruff
ruff check .
ruff format .
```

---

## Performance Notes

`commit.stats` in gitpython runs `git diff --stat` for every commit individually. For repositories with thousands of commits this is the dominant cost. The `--limit` flag is the primary mitigation — keep it below 1000 for interactive use on large repositories.

If you need to analyse very large histories, the natural next step is to batch the stat collection using `git log --numstat` in a single subprocess call rather than per-commit API calls.

## Licence

MIT