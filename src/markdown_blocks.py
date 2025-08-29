import re
from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

# IF SOMETHING BREAKS LATER ON, THIS FUNCTION IS PROBABLY RESPONSIBLE
def block_to_block_type(block):
    # Check for heading block
    if re.search(r'^#{1,6}', block, re.MULTILINE):
        return BlockType.HEADING
    
    # Check for code block
    if re.search(r'```.*?```$', block, re.DOTALL):
        return BlockType.CODE
    
    # Check for quote block
    if re.search(r'(^>.*(\n|$))+', block, re.MULTILINE):
        return BlockType.QUOTE
    
    # Check for unordered list
    if re.search(r'^[-*+]\s', block, re.MULTILINE):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    if re.search(r'^\d+\.\s', block, re.MULTILINE):
        return BlockType.ORDERED_LIST
    
    # If not any of the other block types, then is a paragraph
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    splitted = markdown.split("\n\n")
    splitted_stripped = [line.strip() for line in splitted]
    # this returns blocks
    return [line for line in splitted_stripped if line]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
    
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_to_html_node(block))
            case _:
                raise Exception("something broke, unknown block type")

    return ParentNode("div", children, None)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return children

def paragraph_to_html_node(block):
    paragraph = ' '.join(block.split())
    return ParentNode("p", text_to_children(paragraph))

def heading_to_html_node(block):
    heading = 0
    while heading < len(block) and block[heading] == '#':
        heading += 1
    if heading > 6 or not heading:
        raise ValueError(f'Invalid heading level: {heading}')
    return ParentNode(f'h{heading}', text_to_children(block[heading:].lstrip()))

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError('invalid code block')
    
    content = block[4:-3]
    
    # Split into lines, strip leading whitespace from each line, rejoin
    lines = content.split('\n')
    stripped_lines = [line.lstrip() for line in lines]
    content = '\n'.join(stripped_lines)

    raw_code_text = TextNode(content, TextType.TEXT)
    code_node = text_node_to_html_node(raw_code_text)
    child_node = ParentNode("code", [code_node])
    return ParentNode("pre", [child_node])

def ordered_list_to_html_node(block):
    items = block.split('\n')
    html_items = []

    # 1.
    for item in items:
        item_text = item[3:]
        html_items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", html_items)

def unordered_list_to_html_node(block):
    items = block.split('\n')
    html_items = []

    # - 
    for item in items:
        item_text = item[2:]
        html_items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split('\n')
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError('invalid quote block')
        new_lines.append( line.lstrip(">").strip() )
    content = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(content))