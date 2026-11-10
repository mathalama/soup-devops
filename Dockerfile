# Digest pinning and real Docker execution are pending; this image is a test harness.
FROM python:3.12-slim
WORKDIR /verify
COPY requirements-dev.txt .
RUN python -m pip install --no-cache-dir --require-hashes -r requirements-dev.txt
COPY scripts/check_artifact.py scripts/check_artifact.py
COPY dist/ dist/
RUN python -c "from pathlib import Path; import subprocess,sys; [subprocess.run([sys.executable,'scripts/check_artifact.py',str(p),'--build-tools','requirements-dev.txt'],check=True) for p in Path('dist').iterdir()]"
