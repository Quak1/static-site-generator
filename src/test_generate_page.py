import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_header(self):
        title = extract_title("# Hello")
        self.assertEqual(title, "Hello")

    def test_multiline(self):
        title = extract_title(
            """
# Hello
some content here
"""
        )
        self.assertEqual(title, "Hello")
