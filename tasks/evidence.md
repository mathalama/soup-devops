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

Subsequently hardened sdist installation: build tools now install from requirements-dev.txt
with --require-hashes, and pip builds with --no-build-isolation. Local
`python scripts/check_distributions.py` passed both distributions under that policy.

## Actual Actions experiments (commit 8a0f163)

| Incident | Naive source check | Hardened installed check | Observed failure |
| --- | --- | --- | --- |
| Python 3.10 | [GREEN](https://github.com/mathalama/soup-devops/actions/runs/42808850489) | [RED](https://github.com/mathalama/soup-devops/actions/runs/42808857753) | No module named tomllib on Python 3.10 |
| Windows | [GREEN](https://github.com/mathalama/soup-devops/actions/runs/42808864297) | [RED](https://github.com/mathalama/soup-devops/actions/runs/42808870826) | No module named termios on Windows |
| Omitted wheel data | [GREEN](https://github.com/mathalama/soup-devops/actions/runs/42808877338) | [RED](https://github.com/mathalama/soup-devops/actions/runs/42808886455) | Installed greeting.txt missing |
| Broken console entry point | [GREEN](https://github.com/mathalama/soup-devops/actions/runs/42809106795) | [RED](https://github.com/mathalama/soup-devops/actions/runs/42808940403) | ImportError for missing_main |

Fixed package: [GREEN](https://github.com/mathalama/soup-devops/actions/runs/42808827101).
All nine installed lanes passed: Linux, Windows, macOS x Python 3.10/3.12/3.14.
Build/lint and Docker also passed. Publish was correctly skipped on a branch push.
Latest workflow expands coverage to 3.11 and 3.13 as well; its result is not yet claimed here.

Experiment dispatch: one GitHub GraphQL request timed out before creating the naive entry-point
run. Retried only that dispatch with an explicit main ref, creating run 42809106795.
No failed run was deleted or hidden.

## Subsequent checks
- `uv run --locked ruff check .` and full source suite: passed after adding documentation and workflow improvements.
- GitHub environment testpypi: configured with a custom deployment policy permitting tag `v*` only.
- Added TestPyPI byte verification: three contract tests first failed because module was absent; green result recorded after implementation.
- Two-page PDF generated. Bundled MiKTeX pdftoppm could not render because its setup is incomplete; switched to pypdfium2 without modifying the TeX installation.
- Initial environment API update using stdin JSON failed (400 parse error); nested typed gh fields succeeded. No partial environment rule is claimed from the failed call.
- Two pushes hit GitHub connection timeouts; the subsequent HTTP/1.1 push succeeded and remote commit was confirmed as 27b644a.
