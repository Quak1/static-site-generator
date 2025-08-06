import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

```
code block
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "```\ncode block\n```",
            ],
        )

    def test_markdown_to_blocks_many_lines(self):
        md = """
A line



A second line




A third line
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "A line",
                "A second line",
                "A third line",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        md = """ Normal multiline
paragraph with 
some text"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading(self):
        md = """## Heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_fake_heading(self):
        md = """####### Heading"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code(self):
        md = """```
Code
```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        md = """> Quote
> second line"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_bad_quote(self):
        md = """> Quote
no quote
> second line"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list(self):
        md = """- List
- List"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_bad_unordered_list(self):
        md = """- List
no list
- List"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        md = """1. list
20. list"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_bad_ordered_list(self):
        md = """1. list
20. list
no list"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


class TestMarkdownToHTMLBlock(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
    text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph     text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
## This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading</h2></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
    the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\n    the **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> First line
> hello
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>First line\nhello</blockquote></div>",
        )

    def test_u_list(self):
        md = """
- first item
- second item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li></ul></div>",
        )

    def test_o_list(self):
        md = """
1. first
3. third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>third</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
