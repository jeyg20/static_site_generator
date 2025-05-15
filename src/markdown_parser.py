import re
import textwrap
from enum import Enum

from src.htmlnode import HTMLNode, ParentNode
from src.linknode import split_nodes_image, split_nodes_link
from src.textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


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
        if line and not line.startswith(">"):
            return False
    return True


def is_unordered_list(markdown_lines: list[str]) -> bool:
    if all(len(line) > 1 and line.startswith("-") for line in markdown_lines):
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


def text_to_children(text: str) -> list[HTMLNode]:
    children = text_to_textnodes(text)
    list_of_text_node = []
    for child in children:
        list_of_text_node.append(text_node_to_html_node(child))
    return list_of_text_node


def format_heading(heading_block: str) -> ParentNode:
    heading_match = re.match(r"^(#+)\s*(.*)", heading_block)
    heading_level = len(heading_match.group(1))
    heading_text = heading_match.group(2)
    return ParentNode(f"h{heading_level}", text_to_children(heading_text))


def format_code(code_block: str) -> ParentNode:
    codeblock_match = re.match(r"^```(\S*)\s*\n(.*?)```$", code_block, re.DOTALL)
    code_node = [text_node_to_html_node(TextNode(codeblock_match.group(2), TextType.CODE))]
    return ParentNode("pre", code_node)


def format_quote(quote_block: str) -> ParentNode:
    quote_text = " ".join(list(map(lambda line: line.lstrip("> "), quote_block.split("\n"))))
    return ParentNode("blockquote", text_to_children(quote_text))


def format_unordered_list(list_block: str) -> ParentNode:
    list_text = list(map(lambda line: line.lstrip("- "), list_block.split("\n")))
    unordered_list = []
    for line in list_text:
        unordered_list.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", unordered_list)


def format_ordered_list(list_block: str) -> ParentNode:
    ordered_list = []
    for line in list_block.split("\n"):
        match = re.match(r"^\d+\.\s+", line)

        list_item_text = line

        if match:
            marker_end_index = match.end()
            list_item_text = line[marker_end_index:].strip()
        item_children = text_to_children(list_item_text)

        li_node = ParentNode("li", item_children)
        ordered_list.append(li_node)

    return ParentNode("ol", ordered_list)


def format_paragraph(paragraph_block: str):
    single_line_text = paragraph_block.replace("\n", " ")
    return ParentNode("p", text_to_children(single_line_text))


def markdown_to_html_node(markdown: str) -> HTMLNode:
    parent_node = ParentNode(tag="div", children=[])

    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                parent_node.children.append(format_heading(block))
            case BlockType.CODE:
                parent_node.children.append(format_code(block))
            case BlockType.QUOTE:
                parent_node.children.append(format_quote(block))
            case BlockType.UNORDERED_LIST:
                parent_node.children.append(format_unordered_list(block))
            case BlockType.ORDERED_LIST:
                parent_node.children.append(format_ordered_list(block))
            case BlockType.PARAGRAPH:
                parent_node.children.append(format_paragraph(block))

    return parent_node


if __name__ == "__main__":
    md = textwrap.dedent(
        """
        # Project Overview

        This project aims to convert markdown text into HTML. It supports several basic markdown features. but for it 
        should handle long text like: Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.

        ## Features

        - Headings (h1-h6)
        - Paragraphs
        - **Bold** and _italic_ text
        - `Code` and code blocks
        - [Links](https://www.example.com)
        - ![Image](https://i.pinimg.com/736x/6a/f3/e6/6af3e62223e9fdb0eef596482a1cf5df.jpg)

        ### Getting Started

        Clone the repository:

        ```bash
        git clone https://github.com/your-username/your-repo.git
        cd your-repo
        ```

        Run the conversion script:

        ```python
        python main.py input.md output.html
        def my_func(text: str) -> None:
            for _ in range(10):
                print(randomval, _)
        ```

        > This is a single-line quote.

        > This is a
        > multi-line quote.
        > another line
        > morelines
        > and a extra line

        1. This is an ordered list.
        2. It has multiple items.
        3. Need this list to.
        4. Have more items.
        5. For no reason.


        - And can potentially contain
        - An unordered sub-list (if your parser handles nesting).
        """
    )

    test_md = textwrap.dedent(
        """
        > This is a single-line quote.
        >
        > This is a
        > multi-line quote.
        """
    )

    node = markdown_to_html_node(test_md)
    print(node.to_html())
