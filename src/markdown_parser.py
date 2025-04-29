from enum import Enum

from src.linknode import split_nodes_image, split_nodes_link
from src.textnode import TextNode, TextType, split_nodes_delimiter


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts a raw text string into a list of TextNode objects by
    processing markdown elements (images, links, bold, italic, code).

    Args:
        text: The raw text string to convert.

    Returns:
        A list of TextNode objects representing the parsed text.
    """
    initial_nodes = [TextNode(text, TextType.TEXT)]

    nodes_after_images = split_nodes_image(initial_nodes)

    nodes_after_links = split_nodes_link(nodes_after_images)

    nodes_after_code = split_nodes_delimiter(nodes_after_links, "`", TextType.CODE)

    nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)

    nodes_after_italic = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)

    return nodes_after_italic


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Splits a markdown string into a list of blocks based on blank lines.

    Args:
        markdown: The raw markdown string document

    Returns:
        A list of strings, where each string represents a markdown block separated by one or more blank lines.
    """
    if not markdown.strip():
        return []
    markdown_blocks = [word.strip() for word in markdown.split("\n\n") if word.strip()]
    return markdown_blocks


def block_to_block_type(markdown_block: str) -> BlockType:
    """Identifies the type of markdown block."""
    title_types = ("#", "##", "###", "####", "#####", "######")
    if markdown_block.startswith(title_types):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif markdown_block.startswith(">"):
        return BlockType.QUOTE
    elif markdown_block.startswith("- ") or markdown_block.startswith("* "):
        return BlockType.UNORDERED_LIST
    if markdown_block.startswith("1. "):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
