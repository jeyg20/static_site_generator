import unittest

from htmlnode import HTMLNode, LeafNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node_cannot_have_children(self):
        child = HTMLNode(tag="span", value="I'm a child")

        with self.assertRaises(ValueError) as cm:
            LeafNode(value="Parent", children=[child])

        expected_message = "LeafNode cannot have children"
        self.assertEqual(str(cm.exception), expected_message)


if __name__ == "__main__":
    unittest.main()
