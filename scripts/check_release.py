"""Reject stale files and tag/version mismatch before making artifacts available."""

import email
import os
from pathlib import Path
import tarfile
import tomllib
import zipfile


version = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
tag = os.environ.get("GITHUB_REF", "")
if tag.startswith("refs/tags/") and tag != f"refs/tags/v{version}":
    raise ValueError(f"Tag {tag} does not match package version {version}")
artifacts = sorted(Path("dist").iterdir())
if len(artifacts) != 2:
    raise ValueError("Expected exactly two freshly built distributions")
for artifact in artifacts:
    if artifact.suffix == ".whl":
        with zipfile.ZipFile(artifact) as archive:
            names = [n for n in archive.namelist() if n.endswith(".dist-info/METADATA")]
            if len(names) != 1:
                raise ValueError("Expected exactly one wheel metadata file")
            metadata = archive.read(names[0])
    elif artifact.name.endswith(".tar.gz"):
        with tarfile.open(artifact) as archive:
            names = [n for n in archive.getnames() if n.count("/") == 1 and n.endswith("/PKG-INFO")]
            if len(names) != 1:
                raise ValueError("Expected exactly one sdist metadata file")
            metadata = archive.extractfile(names[0]).read()
    else:
        raise ValueError(f"Unexpected artifact {artifact}")
    message = email.message_from_bytes(metadata)
    if message["Version"] != version:
        raise ValueError(f"Stale artifact {artifact}")
    if message.get_all("Requires-Dist"):
        raise ValueError("This demo must remain runtime dependency-free")
print(f"PASS: distribution versions match source {version} and release tag (if present)")
