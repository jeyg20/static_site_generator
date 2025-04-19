import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        actual_output = node.props_to_html()
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
