import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_str(self):
        node = TextNode("Other text node", TextType.LINK, "example.com")
        self.assertEqual(str(node), "TextNode(Other text node, link, example.com)")


if __name__ == "__main__":
    unittest.main()
