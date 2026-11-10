import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.verify_index import verify_bytes


class IndexIntegrityTests(unittest.TestCase):
    def test_accepts_exact_tested_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / "release.whl"
            expected.write_bytes(b"tested wheel")
            verify_bytes(b"tested wheel", expected, hashlib.sha256(b"tested wheel").hexdigest())

    def test_rejects_changed_bytes_even_if_index_digest_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / "release.whl"
            expected.write_bytes(b"tested wheel")
            with self.assertRaises(ValueError):
                verify_bytes(b"substitute", expected, hashlib.sha256(b"substitute").hexdigest())

    def test_rejects_incorrect_index_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / "release.whl"
            expected.write_bytes(b"tested wheel")
            with self.assertRaises(ValueError):
                verify_bytes(b"tested wheel", expected, "0" * 64)
