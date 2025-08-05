import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
