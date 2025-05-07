import textwrap
from enum import Enum

from src.htmlnode import HTMLNode, LeafNode, ParentNode
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


def is_heading(markdown_block: str) -> bool:
    title_types = ("# ", "## ", "### ", "#### ", "##### ", "###### ")

    if len(markdown_block) < 1:
        return False

    return any(markdown_block.startswith(prefix) for prefix in title_types)


def is_code_block(markdown_block: str) -> bool:
    return markdown_block.startswith("```") and markdown_block.endswith("```")


def is_quote_block(markdown_lines: list[str]) -> bool:
    for line in markdown_lines:
        if line and not line.startswith("> "):
            return False
    return True


def is_unordered_list(markdown_lines: list[str]) -> bool:
    if all(len(line) > 1 and line.startswith("- ") for line in markdown_lines):
        return True
    return False


def is_ordered_list(markdown_lines: list[str]) -> bool:
    non_empty_lines_with_indices = [(i, line) for i, line in enumerate(markdown_lines) if line]

    if not non_empty_lines_with_indices:
        return False

    return all(line.startswith(f"{i + 1}. ") for i, line in non_empty_lines_with_indices)


def block_to_block_type(markdown_block: str) -> BlockType:
    markdown_lines = markdown_block.split("\n")
    if is_heading(markdown_block):
        return BlockType.HEADING

    if is_code_block(markdown_block):
        return BlockType.CODE

    if is_quote_block(markdown_lines):
        return BlockType.QUOTE

    if is_unordered_list(markdown_lines):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(markdown_lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    split_md_blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode(tag="div", children=[])

    for block in split_md_blocks:
        block_type = block_to_block_type(block)
        new_child = LeafNode()
        new_parent = ParentNode(children=[])

        match block_type:
            case BlockType.HEADING:
                heading_type = block.count("#")
                if 1 <= heading_type <= 6:
                    new_child.tag = f"h{heading_type}"
                    new_child.value = block[heading_type:].strip()
            case BlockType.CODE:
                new_child.tag = "code"
                new_child.value = block.strip("```").strip("\n")

                new_parent.tag = "pre"
                new_parent.children = [new_child]

            case BlockType.QUOTE:
                new_child.tag = "blockquote"
                new_child.value = "\n".join([line.strip(">").strip() for line in block.split("\n")])
                parent_node.children.append(new_child)
    return parent_node


def text_to_children(text: str) -> list[HTMLNode]:
    pass


if __name__ == "__main__":
    md = textwrap.dedent(
        """
        # Correct title

        ```
        def foo():
            return False
        ```

        > Wisdom flows
        > like honey
        > from old trees

        - List
        - New item
        - Another item

        1. Wrong start
        2. Skipped again
        3. Fumbled numbers
        """
    )
    for b in markdown_to_blocks(md):
        print(block_to_block_type(b), b.__repr__())
