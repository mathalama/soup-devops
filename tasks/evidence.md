# Observed local evidence

Date: 2026-11-10. Executed by Codex on Windows.

| Command | Observed result |
| --- | --- |
| `python -m unittest discover -s tests -v` with PYTHONPATH=src, before implementation | RED: ModuleNotFoundError, CLI does not yet exist |
| `uv lock` and `uv sync --locked` | Success; uv selected available CPython 3.14.4; 13 resolved packages |
| `uv run --locked ruff check .` | All checks passed (initial implementation) |
| `uv run --locked python -m unittest discover -s tests -v` | 4 passed on Python 3.14.4 |
| `python -m unittest discover -s tests -v` with PYTHONPATH=src | 4 passed on Python 3.10.11 |
| `uv run --locked python -m build --no-isolation` | Built sdist and wheel from sdist, version 0.9.4 |
| `python scripts/check_artifact.py dist/mathalama_soup_release_demo-0.9.4-py3-none-any.whl` | PASS: clean Windows Python 3.10 install, command, bundled data, pip check, version |
| `python scripts/check_artifact.py dist/mathalama_soup_release_demo-0.9.4.tar.gz` | PASS: clean Windows Python 3.10 sdist installation and same checks |
| `docker version --format '{{.Server.Version}}'` | Failed: Docker Desktop Linux engine named pipe unavailable |

No Actions run, Linux/macOS execution, publication, or incident reproduction is claimed by this table.
The sdist installation currently resolves build backend dependencies from the package index;
this must be hardened before release automation is considered complete.
