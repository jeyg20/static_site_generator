import textwrap
import unittest

from src.markdown_parser import markdown_to_blocks, text_to_textnodes
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

    def test_markdown_to_blocks(self):
        md = textwrap.dedent(
            """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        )
        blocks = markdown_to_blocks(md)
        print(blocks)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_basic_paragraphs(self):
        md = textwrap.dedent(
            """
            This is the first paragraph.

            This is the second paragraph.
        """
        )
        expected_blocks = [
            "This is the first paragraph.",
            "This is the second paragraph.",
        ]
        self.assertEqual(markdown_to_blocks(md), expected_blocks)

    def test_paragraph_with_newlines(self):
        md = textwrap.dedent(
            """
            This is the first part of a paragraph.
            This is the second part of the same paragraph.

            This is a new paragraph.
        """
        )
        expected_blocks = [
            "This is the first part of a paragraph.\nThis is the second part of the same paragraph.",
            "This is a new paragraph.",
        ]
        self.assertEqual(markdown_to_blocks(md), expected_blocks)

    def test_multiple_blank_lines(self):
        md = textwrap.dedent(
            """
            Paragraph one.



            Paragraph two with extra blank lines.
        """
        )
        expected_blocks = [
            "Paragraph one.",
            "Paragraph two with extra blank lines.",
        ]
        self.assertEqual(markdown_to_blocks(md), expected_blocks)

    def test_leading_and_trailing_whitespace(self):
        md = textwrap.dedent(
            """

            Paragraph with leading and trailing blank lines.

        """
        )
        expected_blocks = [
            "Paragraph with leading and trailing blank lines.",
        ]
        self.assertEqual(markdown_to_blocks(md), expected_blocks)

    def test_mixed_content(self):
        md = textwrap.dedent(
            """
            # This is a heading

            This is a paragraph with **bold** text.

            - List item one
            - List item two

            ```python
            print("hello")
            ```
        """
        )
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph with **bold** text.",
            "- List item one\n- List item two",
            '```python\nprint("hello")\n```',
        ]
        self.assertEqual(markdown_to_blocks(md), expected_blocks)

    def test_empty_string(self):
        md = ""
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(md), expected_blocks)

    def test_string_with_only_whitespace(self):
        md = "   \n \t\n \n "
        expected_blocks = []
        self.assertEqual(markdown_to_blocks(md), expected_blocks)


if __name__ == "__main__":
    unittest.main()
