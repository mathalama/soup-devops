# Digest observed in the successful Docker Actions run; updates require review.
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
WORKDIR /verify
COPY requirements-dev.txt .
RUN python -m pip install --no-cache-dir --require-hashes -r requirements-dev.txt
COPY scripts/check_artifact.py scripts/check_artifact.py
COPY dist/ dist/
RUN python -c "from pathlib import Path; import subprocess,sys; [subprocess.run([sys.executable,'scripts/check_artifact.py',str(p),'--build-tools','requirements-dev.txt'],check=True) for p in Path('dist').iterdir()]"
