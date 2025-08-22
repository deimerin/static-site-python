import re

def extract_markdown_images(text):
    match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return match
