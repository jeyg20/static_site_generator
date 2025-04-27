import re

from src.textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_with_pattern(old_nodes: list[TextNode], node_type: TextType, extract_func) -> list[TextNode]:
    """
    Splits a list of TextNodes based on a given pattern and creates new nodes
    of a specified type.

    Args:
        old_nodes: The list of TextNodes to split.
        node_type: The TextType for the new nodes created from the matches.
        extract_func: The function to extract the match content (e.g., alt text/url, link text/url).

    Returns:
        A new list of TextNodes.
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        matches = extract_func(text)

        if not matches:
            new_nodes.append(old_node)
            continue

        current_text = text
        for match in matches:
            original_match_string = ""
            if node_type == TextType.IMAGE:
                original_match_string = f"![{match[0]}]({match[1]})"
            elif node_type == TextType.LINK:
                original_match_string = f"[{match[0]}]({match[1]})"

            parts = current_text.split(original_match_string, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            if node_type == TextType.IMAGE:
                new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            elif node_type == TextType.LINK:
                new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))

            current_text = parts[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_with_pattern(old_nodes, TextType.IMAGE, extract_markdown_images)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_with_pattern(old_nodes, TextType.LINK, extract_markdown_links)
