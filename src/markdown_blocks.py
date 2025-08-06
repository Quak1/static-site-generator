from enum import Enum
import re

from htmlnode import ParentNode
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    text_nodes_to_html_nodes,
    text_to_textnodes,
)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(lambda x: x, map(lambda x: x.strip(), blocks)))


def block_to_block_type(block):
    if re.search(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE

    lines = block.split("\n")

    if all(l[0] == ">" for l in lines):
        return BlockType.QUOTE

    if all(l[:2] == "- " for l in lines):
        return BlockType.UNORDERED_LIST

    if all(re.search(r"^\d+\. ", l) for l in lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    children = []

    for block in md_blocks:
        html_block = block_to_html_node(block)
        children.append(html_block)

    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            children = text_nodes_to_html_nodes(
                text_to_textnodes(" ".join(block.split("\n")))
            )
            return ParentNode("p", children)
        case BlockType.HEADING:
            part = block.split(" ", 1)
            children = text_nodes_to_html_nodes(text_to_textnodes(part[1]))
            return ParentNode(f"h{len(part[0])}", children)
        case BlockType.CODE:
            child = text_node_to_html_node(TextNode(block[4:-3], TextType.TEXT))
            return ParentNode("pre", [ParentNode("code", [child])])
        case BlockType.QUOTE:
            content = map(lambda l: l[2:], block.split("\n"))
            child = text_nodes_to_html_nodes(text_to_textnodes("\n".join(content)))
            return ParentNode("blockquote", child)
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", list_block_to_children(block))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", list_block_to_children(block))


def list_block_to_children(block):
    children = map(lambda l: l.split(" ", 1)[1], block.split("\n"))
    children = map(lambda l: text_nodes_to_html_nodes(text_to_textnodes(l)), children)
    children = map(lambda l: ParentNode("li", l), children)
    return list(children)
