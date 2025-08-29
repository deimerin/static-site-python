import re

def extract_markdown_images(text):
    match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return match

def extract_title(markdown):
    title = re.findall(r'^#{1}\s(.*)\n?', markdown, re.MULTILINE)
    if not title:
        raise Exception('Title not found')
    return title[0].strip()