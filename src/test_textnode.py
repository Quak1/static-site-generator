import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)


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


class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This is text with an [link](example.com)")
        self.assertListEqual([("link", "example.com")], matches)

    def test_extract_markdown_link_ignore_image(self):
        matches = extract_markdown_links(
            "This is text with an [link](example.com) ![image](example.com)"
        )
        self.assertListEqual([("link", "example.com")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with multiple [link](example.com)[link2](example.com/2) [link3](example.com/3)"
        )
        self.assertListEqual(
            [
                ("link", "example.com"),
                ("link2", "example.com/2"),
                ("link3", "example.com/3"),
            ],
            matches,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](example.com)")
        self.assertListEqual([("image", "example.com")], matches)

    def test_extract_markdown_images_ignore_link(self):
        matches = extract_markdown_images(
            "This is text with an ![image](example.com) [image](example.com)"
        )
        self.assertListEqual([("image", "example.com")], matches)

    def test_split_no_change(self):
        new_nodes = split_nodes_image(
            [
                TextNode(
                    "This is text",
                    TextType.TEXT,
                ),
                TextNode(
                    "This is bold",
                    TextType.BOLD,
                ),
            ]
        )
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
                TextNode(
                    "This is bold",
                    TextType.BOLD,
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](example.com/1) and ![image2](example.com/2) and another [link](example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "example.com/1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "example.com/2"),
                TextNode(" and another [link](example.com)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](example.com/1) and ![image](example.com) and another [link2](example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "example.com/1"),
                TextNode(" and ![image](example.com) and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "example.com/2"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
