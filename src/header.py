from src.htmlnode import ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node


def generate_nav_bar(dir_names: list[str]) -> ParentNode:
    ordered_list = [
        ParentNode("li", [text_node_to_html_node(TextNode("Home", TextType.LINK, "/"))], {"class": "nav-item"})
    ]
    for dir_name in dir_names:
        a_node = text_node_to_html_node(TextNode(dir_name, TextType.LINK, f"/{dir_name}"))
        li_node = ParentNode("li", [a_node], {"class": "nav-item"})
        ordered_list.append(li_node)

    return ParentNode("ul", ordered_list, {"class": "menu"})
