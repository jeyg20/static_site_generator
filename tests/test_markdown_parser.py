import unittest

from src.markdown_parser import text_to_textnodes
from src.textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_text_with_multiple_elements(self):
        text = "This is **bold** and _italic_ and `code` and a [link](url) and an ![image](url2)."
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url2"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected_nodes)

    def test_text_with_elements_at_start_and_end(self):
        text = "**Start** of text with a [link](url) and an ![image](url2) at the `end`."
        expected_nodes = [
            TextNode("Start", TextType.BOLD),
            TextNode(" of text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url2"),
            TextNode(" at the ", TextType.TEXT),
            TextNode("end", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected_nodes)

    def test_text_with_consecutive_elements(self):
        text = "**Bold**_italic_`code`[link](url)![image](url2)"
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("link", TextType.LINK, "url"),
            TextNode("image", TextType.IMAGE, "url2"),
        ]

        self.assertEqual(text_to_textnodes(text), expected_nodes)


# If you're using unittest's default runner
if __name__ == "__main__":
    unittest.main()
