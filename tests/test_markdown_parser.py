import textwrap
import unittest

from src.markdown_parser import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    text_to_textnodes,
)
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

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a regular paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("This is a paragraph with internal spaces."), BlockType.PARAGRAPH)

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```python\nprint('hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote."), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Multiple\n> lines\n> of quote."), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Some preceding text"), BlockType.ORDERED_LIST)

    def test_mixed_blocks(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph that starts with - but isn't a list."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("This is a paragraph that starts with > but isn't a quote."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("This is a paragraph that starts with 1. but isn't an ordered list."),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("This is a paragraph that contains ``` in the middle."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("This block has -\n> and a quote style line\n1. and an ordered list line"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("- Unordered list line\nThis block also has paragraph text."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. Ordered list line\nThis block also has paragraph text."), BlockType.PARAGRAPH
        )

    def test_paragraphs(self):
        md = textwrap.dedent(
            """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with "
            "<i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = textwrap.dedent(
            """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
