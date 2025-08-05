import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
import textnode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, "example.com")
        node2 = TextNode("This is a text node", TextType.TEXT, "example2.com")
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Other text node", TextType.LINK, "example.com")
        self.assertEqual(repr(node), "TextNode(Other text node, link, example.com)")


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "example.com"})
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props, {"src": "example.com", "alt": "This is a text node"}
        )
        self.assertEqual(html_node.value, "")


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_empty_substring(self):
        node = TextNode("This is __ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_missing_delimiter(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("_italic text_", TextType.TEXT),
            TextNode("no change", TextType.TEXT),
            TextNode("**no change**", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("italic text", TextType.ITALIC),
                TextNode("no change", TextType.TEXT),
                TextNode("**no change**", TextType.ITALIC),
            ],
        )


if __name__ == "__main__":
    unittest.main()
