import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)

def split_nodes_delimiter(nodes, delimiter, target_type):
    new_nodes = []

    for node in nodes:
        if node.text_type == "text":
            text = node.text
            parts = text.split(delimiter)

            # Check if there are an even number of delimiters
            if len(parts) % 2 == 0:
                raise ValueError("Invalid Markdown syntax: missing closing delimiter")

            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:  # Avoid adding empty text nodes
                        new_nodes.append(TextNode(part, "text"))
                else:
                    if part:  # Avoid adding empty target type nodes
                        new_nodes.append(TextNode(part, target_type))
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    # Validate that all matches have proper closing parenthesis
    for match in matches:
        alt_text, url = match
        if not text.count("![{0}]({1})".format(alt_text, url)):
            raise ValueError("Invalid Markdown syntax: missing closing parenthesis")
    return matches

def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(nodes):
    new_nodes = []

    for node in nodes:
        if node.text_type == "text":
            text = node.text
            
            if text == "":
                new_nodes.append(node)
                continue
            
            images = extract_markdown_images(text)
            if not images:
                new_nodes.append(node)
                continue

            last_index = 0

            for alt_text, url in images:
                match_str = f"![{alt_text}]({url})"
                start_index = text.find(match_str, last_index)
                if start_index == -1:
                    continue

                if start_index > last_index:
                    new_nodes.append(TextNode(text[last_index:start_index], "text"))
                
                new_nodes.append(TextNode(alt_text, "image", url))
                last_index = start_index + len(match_str)

            if last_index < len(text):
                new_nodes.append(TextNode(text[last_index:], "text"))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(nodes):
    new_nodes = []

    for node in nodes:
        if node.text_type == "text":
            if node.text == "":
                new_nodes.append(TextNode("", "text"))
            else:
                links = extract_markdown_links(node.text)
                remaining_text = node.text

                for link_text, url in links:
                    split_text = remaining_text.split(f"[{link_text}]({url})", 1)
                    
                    # Add the text before the link
                    if split_text[0]:
                        new_nodes.append(TextNode(split_text[0], "text"))
                    
                    # Add the link
                    new_nodes.append(TextNode(link_text, "link", url))
                    
                    # Remaining text after the link
                    remaining_text = split_text[1] if len(split_text) > 1 else ""

                # Add any remaining text after the last link
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, "text"))
        else:
            new_nodes.append(node)
    
    return new_nodes

# def text_to_textnodes(text):
#     nodes = [TextNode(text, text_type_text)]
#     nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
#     nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
#     nodes = split_nodes_delimiter(nodes, "`", text_type_code)
#     nodes = split_nodes_image(nodes)
#     nodes = split_nodes_link(nodes)
#     return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
