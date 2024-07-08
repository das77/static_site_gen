from htmlnode import (
    LeafNode,
    ParentNode
)

# Block type constants
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "heading":
        return create_heading_node(block)
    elif block_type == "paragraph":
        return create_paragraph_node(block)
    elif block_type == "code":
        return create_code_node(block)
    elif block_type == "quote":
        return create_quote_node(block)
    elif block_type == "unordered_list":
        return create_unordered_list_node(block)
    elif block_type == "ordered_list":
        return create_ordered_list_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def create_heading_node(block):
    level = len(block.split()[0])
    text = block[level+1:].strip()
    return LeafNode(f"h{level}", text)

def create_paragraph_node(block):
    return LeafNode("p", block)

def create_code_node(block):
    code_content = block.strip('```').strip()
    return ParentNode("pre", [LeafNode("code", code_content)])

def create_quote_node(block):
    quote_content = block[1:].strip()
    return ParentNode("blockquote", [LeafNode("p", quote_content)])

def create_unordered_list_node(block):
    items = block.split('\n')
    children = [LeafNode("li", item[1:].strip()) for item in items if item]
    return ParentNode("ul", children)

def create_ordered_list_node(block):
    items = block.split('\n')
    children = [LeafNode("li", item[item.find(' ') + 1:].strip()) for item in items if item]
    return ParentNode("ol", children)