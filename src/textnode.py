from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:

    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if (
            self.text == value.text and
            self.text_type == value.text_type and
            self.url == value.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    
    match text_node.text_type.value:
        case "plain":
            return LeafNode(None, text_node.text)
        
        case "bold":
            return LeafNode("b", text_node.text)

        case "italic":
            return LeafNode("i", text_node.text)

        case "code":
            return LeafNode("code", text_node.text)
        
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

        case _: # Default case - Type not found
            raise Exception("Type not found")
