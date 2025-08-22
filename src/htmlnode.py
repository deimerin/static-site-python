from enum import Enum

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        else:
            attr_string = ""
            for attr in self.props.keys():
                attr_string = attr_string + f'{attr}="{self.props[attr]}" '
            return attr_string[:-1]
    
    def __repr__(self):
        return f"HTMLNode( Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{' '+self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No children")
        
        return f'<{self.tag}{" "+self.props_to_html() if self.props else ""}>{"".join(child.to_html() for child in self.children)}</{self.tag}>'
        