from enum import Enum

from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

    # Added for clarity in error messages
    @classmethod
    def values(cls):
        return [member.value for member in cls]


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = ""):

        if not isinstance(text_type, TextType):
            raise TypeError(f"text_type must be a member of the TextType Enum, not {type(text_type)}")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("text_type must be a member of the TextType Enum")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)

        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)

        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)

        case TextType.LINK:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props={"href": text_node.url},
            )

        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            valid_string_values = [member.value for member in TextType]
            raise ValueError(
                f"Invalid text type string: '{text_node.text_value}' Must be one of: {', '.join(valid_string_values)}"
            )


def split_nodes_delimiter(text_nodes_to_split: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Splits a list of TextNodes based on a given delimiter and creates new nodes
    with the specified text type for the content within the delimiters.

    Args:
        text_nodes_to_split: The list of TextNodes to split.
        delimiter: The markdown delimiter (e.g., '`', '**', '_').
        text_type: The TextType to apply to the content within the delimiters
                   (e.g., TextType.CODE, TextType.BOLD, TextType.ITALIC).

    Returns:
        A new list of TextNodes with content split by the delimiter.

    Raises:
        ValueError: If the delimiter is invalid for the text type, or if a
                    delimiter is not properly closed.
    """

    valid_pairs = {
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
    }

    if (delimiter, text_type) not in valid_pairs:
        raise ValueError(f"Invalid markdown syntax: Delimiter '{delimiter}' is not valid for text type '{text_type}'")

    split_nodes = []

    for node in text_nodes_to_split:
        if node.text_type is not TextType.TEXT:
            split_nodes.append(node)
            continue

        segments = node.text.split(delimiter)
        if len(segments) % 2 != 1:
            raise ValueError(f"Invalid markdown syntax: Delimiter '{delimiter}' was never closed in text: {node.text}")
        for index, item in enumerate(segments):
            if item == "":
                continue
            if index % 2 == 0:
                split_nodes.append(TextNode(item, TextType.TEXT))
            else:
                split_nodes.append(TextNode(item, text_type))

    return split_nodes
