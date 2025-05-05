class HTMLNode:
    """
    Represents a node in an HTML tree structure.
    This is the base class for different types of HTML nodes.
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        """
        Initializes an HTMLNode.

        Args:
            tag (str | None): The HTML tag name (e.g., "p", "div", "a"). Defaults to None.
            value (str | None): The value of the HTML tag (e.g., the text content for a paragraph).
                                 Defaults to None.
            children (list["HTMLNode"] | None): A list of HTMLNode objects that are children
                                                of this node. Defaults to None.
            props (dict[str, str] | None): A dictionary of key-value pairs representing the
                                           attributes of the HTML tag (e.g., {"href": "google.com"}).
                                           Defaults to None.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the HTMLNode to its HTML string representation.
        This method should be implemented by subclasses.

        Raises:
            NotImplementedError: This method is not implemented in the base class
                                 and must be overridden by subclasses.
        """
        raise NotImplementedError

    def props_to_html(self) -> str:
        """
        Converts the props dictionary into a string of HTML attributes.

        Example:
            If self.props is {"href": "google.com", "target": "_blank"},
            this method returns ' href="google.com" target="_blank"'.
            Handles escaping double quotes in attribute values.

        Returns:
            str: A string representation of the HTML attributes, prefixed with a space,
                 or an empty string if no props exist.
        """
        if not self.props:
            return ""
        props_parts = []
        for key, value in self.props.items():
            # Escape double quotes in attribute values
            escaped_value = value.replace('"', "&quot;")
            props_parts.append(f'{key}="{escaped_value}"')

        return " " + " ".join(props_parts)

    def __repr__(self) -> str:
        """
        Returns a string representation of the HTMLNode for debugging purposes.
        """
        return (
            f"HTMLNode("
            f"tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={self.props}"
            f")"
        )


class LeafNode(HTMLNode):
    """
    Represents an HTML node that contains a value but no children (e.g., text, img, a with text).
    Inherits from HTMLNode.
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ):
        """
        Initializes a LeafNode.

        Args:
            tag (str | None): The HTML tag name (e.g., "p", "span", "img"). Defaults to None
                                for plain text nodes.
            value (str | None): The value of the HTML tag (e.g., the text content). Must
                                 be provided for LeafNodes. Defaults to None.
            props (dict[str, str] | None): A dictionary of key-value pairs for attributes.
                                           Defaults to None.
        """

        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        """
        Converts the LeafNode to its HTML string representation.

        Returns:
            str: The HTML string for the leaf node. If tag is None, returns the raw value.

        Raises:
            ValueError: If the LeafNode is initialized without a value.
        """
        if not self.value:
            raise ValueError("LeafNode requires a value to render HTML")

        if not self.tag:
            return str(self.value)

        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """
    Represents an HTML node that contains children nodes but no direct value (e.g., div, p, ul).
    Inherits from HTMLNode.
    """

    def __init__(
        self,
        tag: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        """
        Initializes a ParentNode.

        Args:
            tag (str): The HTML tag name (e.g., "div", "p", "ul"). Must be provided for ParentNodes.
            children (list["HTMLNode"]): A list of HTMLNode objects that are children
                                         of this node. Must be provided for ParentNodes.
            props (dict[str, str] | None): A dictionary of key-value pairs for attributes.
                                           Defaults to None.
        """

        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """
        Converts the ParentNode to its HTML string representation by recursively
        rendering its children.

        Returns:
            str: The HTML string for the parent node and its children.

        Raises:
            ValueError: If the ParentNode is initialized without a tag or children.
        """
        if not self.tag:
            raise ValueError("ParentNode requires a tag to render HTML")

        # Check if children is a list and is not empty
        if not self.children or not isinstance(self.children, list) or len(self.children) == 0:
            raise ValueError("ParentNode requires children (a list of HTMLNode objects) to render HTML")

        props_string = self.props_to_html()
        opening_tag = f"<{self.tag}{props_string}>"

        children_string = ""
        # Recursively render children
        for child in self.children:
            children_string += child.to_html()

        closing_tag = f"</{self.tag}>"

        return f"{opening_tag}{children_string}{closing_tag}"
