"""Download TestPyPI distributions, compare tested bytes, then exercise both."""

import hashlib
import json
from pathlib import Path
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen


def verify_bytes(data, expected, advertised_digest):
    actual = hashlib.sha256(data).hexdigest()
    tested = hashlib.sha256(expected.read_bytes()).hexdigest()
    if actual != advertised_digest or actual != tested:
        raise ValueError(f"Published bytes differ from tested artifact: {expected.name}")


def main():
    from scripts.check_artifact import check

    endpoint = "https://test.pypi.org/pypi/mathalama-soup-release-demo/0.9.4/json"
    for attempt in range(6):
        try:
            with urlopen(endpoint, timeout=30) as response:
                metadata = json.load(response)
            break
        except (HTTPError, URLError) as error:
            if isinstance(error, HTTPError) and error.code != 404:
                raise
            if attempt == 5:
                raise
            time.sleep(10)

    expected = {path.name: path for path in Path("dist").iterdir()}
    if len(expected) != 2:
        raise ValueError("Expected exactly the two tested distributions")
    published = {item["filename"]: item for item in metadata["urls"]}
    if expected.keys() != published.keys():
        raise ValueError("Index filenames do not match tested release")
    with tempfile.TemporaryDirectory(prefix="soup-index-") as directory:
        for filename, source in expected.items():
            item = published[filename]
            url = urlparse(item["url"])
            if url.scheme != "https" or url.hostname != "test-files.pythonhosted.org":
                raise ValueError("Unexpected TestPyPI download host")
            with urlopen(item["url"], timeout=30) as response:
                data = response.read(10 * 1024 * 1024 + 1)
            if len(data) > 10 * 1024 * 1024:
                raise ValueError("Demo artifact unexpectedly large")
            verify_bytes(data, source, item["digests"]["sha256"])
            destination = Path(directory) / filename
            destination.write_bytes(data)
            check(destination, "0.9.4", Path("requirements-dev.txt"))
            print(f"PASS index identity: {filename}")


if __name__ == "__main__":
    main()
