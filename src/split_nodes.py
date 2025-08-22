from textnode import TextType, TextNode
from extract_markdown import extract_markdown_links, extract_markdown_images

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else: 

            splitted = node.text.split(delimiter)

            if len(splitted) % 2 == 0:
                raise Exception(f"Unmatched closing delimiter '{delimiter}' in text: {node.text}")
            else:
                for ind, text in enumerate(splitted):
                    if not text:
                        continue
                    if ind & 1:
                        new_nodes.append(TextNode(text, text_type))
                    else:
                        new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = node.text
        
        while True:
            images = extract_markdown_images(current_text)
            
            if not images:
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                break
            
            image_string = images[0]
            image_markdown = f"![{image_string[0]}]({image_string[1]})"
            sections = current_text.split(image_markdown, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_string[0], TextType.IMAGE, image_string[1]))

            current_text = sections[1]

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = node.text
        
        while True:
            links = extract_markdown_links(current_text)
            
            if not links:
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                break
            
            link_string = links[0]
            link_markdown = f"[{link_string[0]}]({link_string[1]})"
            sections = current_text.split(link_markdown, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_string[0], TextType.LINK, link_string[1]))

            current_text = sections[1]

    return new_nodes