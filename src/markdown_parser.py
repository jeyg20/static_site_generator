from src.linknode import split_nodes_image, split_nodes_link
from src.textnode import TextNode, TextType, split_nodes_delimiter


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
