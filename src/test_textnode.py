import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_equal(self):
        node = TextNode("Same node", TextType.ITALIC)
        node2 = TextNode("Same node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_image(self):
        node = TextNode(
            "Alt text",
            TextType.IMAGE,
            "https://www.example.com/image.png",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.example.com/image.png", "alt": "Alt text"},
        )

    def test_split_code_nodes_delimeter(self):
        nodes = [
            TextNode("`code block` this is text with a `code block` word `code block`", TextType.TEXT),
            TextNode("`second code block`", TextType.TEXT),
            TextNode("word with no delimiter", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("code block", TextType.CODE),
            TextNode(" this is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode("second code block", TextType.CODE),
            TextNode("word with no delimiter", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_bold_nodes_delimiter(self):
        nodes = [
            TextNode("**bold text** interspersed with regular text and **more bold**.", TextType.TEXT),
            TextNode("A separate node with **only bold text**.", TextType.TEXT),
            TextNode("No bold here.", TextType.TEXT),
            TextNode("Starts **with bold**.", TextType.TEXT),
            TextNode("**Ends with bold**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode(" interspersed with regular text and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
            TextNode("A separate node with ", TextType.TEXT),
            TextNode("only bold text", TextType.BOLD),
            TextNode(".", TextType.TEXT),
            TextNode("No bold here.", TextType.TEXT),
            TextNode("Starts ", TextType.TEXT),
            TextNode("with bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
            TextNode("Ends with bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_italic_nodes_delimiter(self):
        nodes = [
            TextNode("_italic text_ alongside normal text.", TextType.TEXT),
            TextNode("Another node with _just italic_.", TextType.TEXT),
            TextNode("Plain text here.", TextType.TEXT),
            TextNode("_Starts with italic_.", TextType.TEXT),
            TextNode("Ends with _italic_", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("italic text", TextType.ITALIC),
            TextNode(" alongside normal text.", TextType.TEXT),
            TextNode("Another node with ", TextType.TEXT),
            TextNode("just italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
            TextNode("Plain text here.", TextType.TEXT),
            TextNode("Starts with italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
            TextNode("Ends with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_missing_closing_delimiter(self):
        nodes = [
            TextNode("text with `open code block", TextType.TEXT),
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_mixed_delimiters_in_input(self):
        nodes = [
            TextNode(" text with `code` and **bold**", TextType.TEXT),
        ]
        # When splitting by '`', the '**bold**' part remains in a TEXT node
        new_nodes_code = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected_nodes_code = [
            TextNode("text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and **bold**", TextType.TEXT),
        ]
        self.assertEqual(new_nodes_code, expected_nodes_code)

        # When splitting by '**', the '`code`' part remains in a TEXT node
        new_nodes_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes_bold = [
            TextNode("text with `code` and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes_bold, expected_nodes_bold)


if __name__ == "__main__":
    unittest.main()
