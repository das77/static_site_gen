class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {prop}="{self.props[prop]}"' for prop in self.props)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('Invalid HTML: no value')
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        def recursive_to_html(node):
            if isinstance(node, LeafNode):
                return node.to_html()
            elif isinstance(node, ParentNode):
                children_html = ""
                if node.children:
                    for child in node.children:
                        children_html += recursive_to_html(child)
                if node.tag:
                    return f"<{node.tag}{node.props_to_html()}>{children_html}</{node.tag}>"
                else:
                    return children_html
        return recursive_to_html(self)