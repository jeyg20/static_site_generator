import unittest

from src.linknode import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from src.textnode import TextNode, TextType


class TestLinkNode(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches
        )

    def test_split_single_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png).", TextType.TEXT)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), expected_nodes)

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another "
            "![second image](https://i.imgur.com/3elNhQu.png).",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), expected_nodes)

    def test_split_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) This is text.", TextType.TEXT)
        expected_nodes = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" This is text.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), expected_nodes)

    def test_split_image_at_end(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(split_nodes_image([node]), expected_nodes)

    def test_split_no_image(self):
        node = TextNode("This is text with no image.", TextType.TEXT)
        expected_nodes = [TextNode("This is text with no image.", TextType.TEXT)]
        self.assertEqual(split_nodes_image([node]), expected_nodes)

    def test_split_image_only(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        expected_nodes = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertEqual(split_nodes_image([node]), expected_nodes)

    def test_split_non_text_node_image(self):
        node = TextNode("Some bold text", TextType.BOLD)
        expected_nodes = [TextNode("Some bold text", TextType.BOLD)]
        self.assertEqual(split_nodes_image([node]), expected_nodes)

    def test_split_single_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev).", TextType.TEXT)
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link([node]), expected_nodes)

    def test_split_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev).",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link([node]), expected_nodes)

    def test_split_link_at_start(self):
        node = TextNode("[to boot dev](https://www.boot.dev) This is text.", TextType.TEXT)
        expected_nodes = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" This is text.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link([node]), expected_nodes)

    def test_split_link_at_end(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(split_nodes_link([node]), expected_nodes)

    def test_split_no_link(self):
        node = TextNode("This is text with no link.", TextType.TEXT)
        expected_nodes = [TextNode("This is text with no link.", TextType.TEXT)]
        self.assertEqual(split_nodes_link([node]), expected_nodes)

    def test_split_link_only(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        expected_nodes = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
        self.assertEqual(split_nodes_link([node]), expected_nodes)

    def test_split_non_text_node_link(self):
        node = TextNode("Some bold text", TextType.BOLD)
        expected_nodes = [TextNode("Some bold text", TextType.BOLD)]
        self.assertEqual(split_nodes_link([node]), expected_nodes)


if __name__ == "__main__":
    unittest.main()
