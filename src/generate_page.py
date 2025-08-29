import os
import sys

from extract_markdown import extract_title
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    # Read markdown file -> from_path
    try:
        with open(from_path, 'r') as markdown_file:
            markdown_content = markdown_file.read()
    except FileNotFoundError:
        print(f'The file {from_path} was not found.')
        sys.exit()

    # Read template file -> template_path
    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f'The template file {template_path} was not found.')
        sys.exit()
    
    # html_node should be a string
    html_node = markdown_to_html_node(markdown_content).to_html()
    page_title = extract_title(markdown_content)
    
    template_content =  template_content.replace("{{ Title }}", page_title)
    template_content =  template_content.replace("{{ Content }}", html_node)

    # Make new html file in the dest_path
    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)

    # Write file content
    with open(dest_path, 'w') as file:
        file.write(template_content)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    current_content_path_items = os.listdir(dir_path_content)

    for item in current_content_path_items:

        # Check extension
        file_name, ext = os.path.splitext(item)

        item_path = os.path.join(dir_path_content, item)

        if os.path.isfile(item_path):
            if ext != '.md':
                continue
            generate_page(item_path, template_path, os.path.join(dest_dir_path, f'{file_name}.html'))
        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item))
     