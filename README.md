# Soup release engineering task

Work in progress. This is independent of Qolda.

## Local checks
Requires Python 3.10+ and uv.

```sh
uv sync --locked
uv run --locked ruff check .
uv run --locked python -m unittest discover -s tests -v
uv run --locked python -m build --no-isolation
python scripts/check_artifact.py dist/*.whl
```

The final command accepts one wheel or sdist path (use its actual filename on Windows).
It installs into a temporary environment outside the source checkout without runtime dependencies,
then runs the installed console command and checks bundled data and version metadata.

## Evidence status
- Source contract tests: see tasks/evidence.md.
- Actions red/green runs: not yet executed.
- Docker verification: Docker engine not currently available.
- TestPyPI publication: not yet configured or executed.

## AI use
Codex read the assignment, proposed the initial design, and generated the initial files.
Local commands and their observed results are recorded in tasks/evidence.md.
The candidate has not yet reviewed or independently verified the implementation;
no claim is made that AI-generated changes were written or verified by the candidate.
