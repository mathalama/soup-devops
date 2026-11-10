"""Deliberate, opt-in failures for evidence runs. Never call during a release."""

import argparse
from pathlib import Path


def inject(root, bug):
    cli = root / "src/soup_release_demo/cli.py"
    config = root / "pyproject.toml"
    if bug in ("python310", "windows"):
        source = cli.read_text(encoding="utf-8")
        module = "tomllib" if bug == "python310" else "termios"
        source = source.replace(
            "def main(argv=None):",
            f"def main(argv=None):\n    __import__({module!r})",
        )
        cli.write_text(source, encoding="utf-8")
    elif bug == "missing-data":
        source = config.read_text(encoding="utf-8")
        source = source.replace(
            '[tool.hatch.build.targets.wheel]',
            '[tool.hatch.build.targets.wheel]\nexclude = ["src/soup_release_demo/greeting.txt"]',
        )
        config.write_text(source, encoding="utf-8")
    elif bug == "entry-point":
        source = config.read_text(encoding="utf-8")
        config.write_text(source.replace("cli:main", "cli:missing_main"), encoding="utf-8")
    elif bug != "fixed":
        raise ValueError(bug)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bug", choices=["fixed", "python310", "windows", "missing-data", "entry-point"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    inject(arguments.root, arguments.bug)
