# htmlnode.py

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.props = props if props else {}

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (self.tag == other.tag and
                    self.value == other.value and
                    self.children == other.children and
                    self.props == other.props)
        return False

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented in child classes")

    def props_to_html(self):
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"