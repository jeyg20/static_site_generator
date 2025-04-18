from textnode import TextNode


def main():
    test_text_node = TextNode(
        "this is some random text", "links", "https://www.boot.dev"
    )
    print(test_text_node)


if __name__ == "__main__":
    main()
