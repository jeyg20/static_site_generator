class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Render the node's props as an HTML string."""
        if not self.props:
            return ""
        props_list = [f'{key}="{value}"' for key, value in self.props.items()]
        return " " + " ".join(props_list)

    def __repr__(self) -> str:
        return (
            f"HTMLNode("
            f"tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={self.props}"
            f")"
        )


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: str | None = None,
        props: dict[str, str] | None = None,
        children: None = None,
    ):
        if children is not None:
            raise ValueError("LeafNode cannot have children")

        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value to render HTML")

        if self.tag is None:
            return str(self.value)
        else:
            props_string = self.props_to_html()
            return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return (
            f"LeafNode("
            f"tag={self.tag}, "
            f"value={self.value}, "
            f"props={self.props}"
            f")"
        )
