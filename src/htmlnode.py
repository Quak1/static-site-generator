class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        html_props = []
        for prop, val in self.props.items():
            html_props.append(f'{prop}="{val}"')
        return " " + " ".join(html_props)

    def __repr__(self) -> str:
        lines = [
            f"HTMLNode(<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>, children="
        ]
        if not self.children:
            lines.append("  None")
        else:
            for child in self.children:
                s = repr(child)
                lines.append("\n".join("  " + line for line in s.splitlines()))

        lines.append(")")
        return "\n".join(lines)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children or len(self.children) == 0:
            raise ValueError("All parent nodes must have children")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
