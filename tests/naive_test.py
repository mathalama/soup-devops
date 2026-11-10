"""Intentionally inadequate: source-only test never invokes installed command."""

import unittest

from soup_release_demo.cli import greeting


class NaiveTest(unittest.TestCase):
    def test_greeting(self):
        self.assertEqual(greeting("Ada"), "Hello, Ada!")
