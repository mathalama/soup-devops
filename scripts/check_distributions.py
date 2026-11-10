"""Verify exactly one wheel and one sdist from the current build."""

from pathlib import Path

from check_artifact import check


artifacts = sorted(Path("dist").iterdir())
if len(artifacts) != 2:
    raise ValueError(f"Expected exactly two distributions, got {artifacts}")
if sum(p.suffix == ".whl" for p in artifacts) != 1:
    raise ValueError("Expected exactly one wheel")
if sum(p.name.endswith(".tar.gz") for p in artifacts) != 1:
    raise ValueError("Expected exactly one sdist")
for artifact in artifacts:
    check(artifact, "0.9.4", Path("requirements-dev.txt"))
