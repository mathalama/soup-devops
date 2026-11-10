# Threat model and controls

Assets: ability to publish a package under the project identity; integrity of the exact files
installed by users; GitHub identity; paid compute budget.
Boundaries: fork source into CI, registry downloads into builds, built files into artifact storage,
artifact storage into publication, repository OIDC identity into TestPyPI.

| Silent failure | Control | Remaining limitation |
| --- | --- | --- |
| Unpinned dependency / substituted release | Runtime dependencies deliberately absent. Build/lint dependencies including transitives exported from uv.lock with SHA256 hashes; pip requires hashes. Actions pinned to full commits. | Approved hashes can still represent malicious upstream software; review origins and updates. |
| Cache hides bad resolution | No dependency, wheel or Docker layer cache is restored for release verification; pip uses --no-cache-dir; Docker uses --no-cache. | Index availability and bootstrap pip/host trust remain. |
| Stale artifact | Fresh runner, exact two distributions, metadata/source version check, current-run-only artifact name includes commit SHA; publish downloads the same files rather than rebuilding. | A compromised build runner or authorized workflow change can substitute artifacts. |
| Fork PR reaches secret | pull_request only, contents:read, checkout credentials disabled, no long-lived publishing token, id-token:write only in tag-push publication job; no source checkout in publish. | Repository writers can edit workflow; account security and environment tag restrictions matter. |
| Version disagrees with tag | Reject tag other than v + project version, check wheel and sdist metadata before upload. | Tag permission policy must prevent unreviewed tags or movement. |

The hash lock narrows dependency substitution; it is not a malware scanner. uv.lock is the
authoritative resolution; requirements-dev.txt is its generated pip-compatible export.
Updates must regenerate and review both together. Export parity enforcement is pending.

OIDC authenticates a workflow identity, not program correctness. Configure only the exact
owner/repository/workflow/environment on TestPyPI. No credentials are needed for matrix tests.
The public TestPyPI index is the only publish destination configured; no real PyPI job exists.

References:
- https://docs.pypi.org/trusted-publishers/using-a-publisher/
- https://docs.pypi.org/trusted-publishers/security-model/
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.astral.sh/uv/concepts/projects/sync/
