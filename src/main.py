from textnode import TextNode, TextType


def main():
    test_node = TextNode(
        "this is some random text", TextType.BOLD, "https://www.boot.dev"
    )
    print(test_node)


if __name__ == "__main__":
    main()
