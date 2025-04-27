import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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

        with self.assertRaises(TypeError) as cm:
            LeafNode(value="Parent", children=[child])

        expected_message = "LeafNode.__init__() got an unexpected keyword argument 'children'"
        self.assertEqual(str(cm.exception), expected_message)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
