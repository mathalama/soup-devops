# Soup release engineering task

Release engineering demonstration: a dependency-free Python greeting CLI, four deliberate
incidents, naive source checks, clean wheel/sdist installation across OS/Python versions,
Docker verification, and a tag-triggered TestPyPI OIDC workflow.

## Local checks
Requires Python 3.10+ and uv.

```sh
uv sync --locked
uv run --locked ruff check .
uv run --locked python -m unittest discover -s tests -v
uv run --locked python -m build --no-isolation
python scripts/check_distributions.py
```

The final command checks exactly one wheel and sdist in dist. It installs into temporary
environments outside the source checkout without runtime dependencies, then runs the installed
console command and checks bundled data and version metadata. The sdist build tools are
installed from the hash-locked export; wheel verification has no development tools installed.

## Experiments
Dispatch both `naive.yml` and `release.yml` with `bug` set to `python310`, `windows`,
`missing-data`, or `entry-point`. The naive workflow should pass every case; hardened should
fail the relevant installed-package job. `fixed` uses unmodified source and should pass all jobs.
Injection happens only in the disposable runner checkout and never publishes an experimental build.
See [evidence](tasks/evidence.md), [supply-chain controls](docs/SUPPLY-CHAIN.md), and
[GPU design](docs/GPU-DESIGN.md). Do not hide or delete failed runs.

## TestPyPI setup
Create a pending trusted publisher on TestPyPI:
- Project: `mathalama-soup-release-demo`
- Owner: `mathalama`, repository: `soup-devops`
- Workflow: `release.yml`, environment: `testpypi`

After trusted-publisher and environment configuration, tag version 0.9.4 as `v0.9.4`.
The tag/version gate runs before publication; publication waits for all installed and Docker jobs.
Only TestPyPI is configured. Do not republish an existing version or delete failed evidence.

## Evidence status
- Source contract tests: see tasks/evidence.md.
- Actions red/green runs: executing; see tasks/evidence.md for confirmed results.
- Docker verification: successful on GitHub-hosted Linux; local Docker engine unavailable.
- TestPyPI publication: not yet configured or executed.

## AI use
Codex read the assignment, proposed the initial design, and generated the initial files.
Local commands and their observed results are recorded in tasks/evidence.md.
The candidate has not yet reviewed or independently verified the implementation;
no claim is made that AI-generated changes were written or verified by the candidate.
