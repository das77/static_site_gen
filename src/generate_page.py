import os
import logging
from htmlnode import HTMLNode
from extract_title import extract_title
from block_markdown import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    :param from_path: Path to the markdown file.
    :param template_path: Path to the template file.
    :param dest_path: Path to save the generated HTML file.
    """
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    
    # Read template file
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    
    # Convert markdown to HTML
    # markdown_node = MarkdownToHtmlNode(markdown_content)
    markdown_node = markdown_to_html_node(markdown_content)
    html_content = markdown_node.to_html()
    
    # Extract title from markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    final_content = template_content.replace('{{ Title }}', title)
    final_content = template_content.replace('{{ Content }}', html_content)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML content to the destination file
    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(final_content)
    
    logging.info(f"Page generated successfully at {dest_path}")