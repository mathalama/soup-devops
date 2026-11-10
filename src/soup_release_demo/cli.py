"""A portable greeting command with bundled package data."""

import argparse
from importlib.resources import files


def greeting(name="world"):
    name = name.strip()
    if not name:
        raise ValueError("name must not be blank")
    template = files("soup_release_demo").joinpath("greeting.txt").read_text(encoding="utf-8")
    return template.strip().format(name=name)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print a greeting")
    parser.add_argument("--name", default="world")
    args = parser.parse_args(argv)
    try:
        result = greeting(args.name)
    except ValueError as error:
        parser.error(str(error))
    print(result)
    return 0
