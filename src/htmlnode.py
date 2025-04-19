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
        if not self.props:
            return ""
        props_parts = []
        for key, value in self.props.items():
            escaped_value = value.replace('"', "&quot;")
            props_parts.append(f'{key}="{escaped_value}"')

        return " " + " ".join(props_parts)

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
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ):

        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode requires a value to render HTML")

        if not self.tag:
            return str(self.value)

        else:
            props_string = self.props_to_html()
            return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ):

        super().__init__(tag=tag, value=None, children=children, props=None)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires a tag to render HTML")

        if not self.children or not isinstance(self.children, list):
            raise ValueError("ParentNode requires a children to render HTML")

        props_string = self.props_to_html()
        opening_tag = f"<{self.tag}{props_string}>"

        children_string = ""
        for child in self.children:
            children_string += child.to_html()

        closing_tag = f"</{self.tag}>"

        return f"{opening_tag}{children_string}{closing_tag}"
