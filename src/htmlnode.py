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
