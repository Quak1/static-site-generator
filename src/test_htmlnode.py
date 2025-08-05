import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_default(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_not_implemented(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "example.com", "title": "Example site"})
        self.assertEqual(
            node.props_to_html(), ' href="example.com" title="Example site"'
        )

    def test_repr(self):
        child_node = HTMLNode(tag="p", value="child", children=[HTMLNode(tag="a")])
        node = HTMLNode(
            tag="a",
            value="example",
            props={"href": "example.com", "title": "Example site"},
            children=[child_node, HTMLNode(value="second")],
        )
        self.assertEqual(
            repr(node),
            """HTMLNode(<a href="example.com" title="Example site">example</a>, children=
  HTMLNode(<p>child</p>, children=
    HTMLNode(<a>None</a>, children=
      None
    )
  )
  HTMLNode(<None>second</None>, children=
    None
  )
)""",
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_props(self):
        node = LeafNode("a", "Hello, world!", {"href": "example.com"})
        self.assertEqual(node.to_html(), '<a href="example.com">Hello, world!</a>')

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child2_node = LeafNode(None, "second child")
        parent_node = ParentNode("div", [child_node, child2_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child</span>second child</div>"
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode(None, "Hello")
        parent_node = ParentNode("", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_no_child(self):
        grandparent_node = ParentNode("div", None)
        parent_node = ParentNode("p", [grandparent_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_grandchildren_props(self):
        child_node = ParentNode(
            "li",
            [
                LeafNode("b", "Bold text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        child_node2 = ParentNode(
            "li",
            [
                LeafNode(
                    None,
                    "Child 2",
                )
            ],
            {"class": "hello"},
        )
        child_node3 = ParentNode("li", [child_node2])
        parent_node = ParentNode("ul", [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            '<ul><li><b>Bold text</b><i>italic text</i>Normal text</li><li class="hello">Child 2</li><li><li class="hello">Child 2</li></li></ul>',
        )


if __name__ == "__main__":
    unittest.main()
