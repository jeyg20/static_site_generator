from src.htmlnode import LeafNode, ParentNode
from src.textnode import TextNode, TextType


def main():
    test_node = TextNode("this is some random text", TextType.BOLD, "https://www.boot.dev")
    print(test_node)

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())


if __name__ == "__main__":
    main()
