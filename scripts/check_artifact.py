"""Exercise an installed distribution with no source checkout on sys.path."""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import venv


def check(artifact, expected_version, build_tools=None):
    artifact = artifact.resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix="soup-installed-") as directory:
        root = Path(directory)
        environment = root / "venv"
        venv.EnvBuilder(with_pip=True).create(environment)
        binary = environment / ("Scripts" if os.name == "nt" else "bin")
        python = binary / ("python.exe" if os.name == "nt" else "python")
        command = binary / ("soup-demo.exe" if os.name == "nt" else "soup-demo")
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)

        def run(*args):
            result = subprocess.run(
                [str(arg) for arg in args], cwd=root, env=env,
                text=True, capture_output=True, encoding="utf-8",
            )
            if result.returncode:
                print(result.stdout)
                print(result.stderr)
                result.check_returncode()
            return result

        # No fallback index and no runtime dependency resolution for this dependency-free CLI.
        if artifact.name.endswith(".tar.gz"):
            if build_tools is None:
                raise ValueError("sdist verification requires --build-tools requirements-dev.txt")
            run(python, "-m", "pip", "install", "--require-hashes", "--no-cache-dir",
                "-r", build_tools.resolve(strict=True))
        run(python, "-m", "pip", "install", "--no-deps", "--no-cache-dir",
            "--no-build-isolation", artifact)
        run(python, "-m", "pip", "check")
        assert run(command, "--name", "Ada").stdout.strip() == "Hello, Ada!"
        assert run(command).stdout.strip() == "Hello, world!"
        metadata = run(
            python, "-I", "-c",
            "from importlib.metadata import version; "
            "print(version('mathalama-soup-release-demo'))",
        ).stdout.strip()
        assert metadata == expected_version, (metadata, expected_version)
        print(f"PASS {artifact.name}: installed CLI, data, dependencies, version {metadata}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--version", default="0.9.4")
    parser.add_argument("--build-tools", type=Path)
    args = parser.parse_args()
    check(args.artifact, args.version, args.build_tools)
