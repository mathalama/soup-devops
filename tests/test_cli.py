import contextlib
import io
import unittest

from soup_release_demo.cli import greeting, main


class GreetingTests(unittest.TestCase):
    def test_default_name(self):
        self.assertEqual(greeting(), "Hello, world!")

    def test_unicode_name(self):
        self.assertEqual(greeting("Әлия"), "Hello, Әлия!")

    def test_blank_name_is_rejected(self):
        with self.assertRaises(ValueError):
            greeting("   ")

    def test_cli_prints_greeting(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["--name", "Ada"]), 0)
        self.assertEqual(output.getvalue(), "Hello, Ada!\n")


if __name__ == "__main__":
    unittest.main()
