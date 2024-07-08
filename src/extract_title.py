def extract_title(markdown):
    """
    Extract the text of the H1 header from the markdown content.
    
    :param markdown: String containing the markdown content.
    :return: Text of the H1 header.
    :raises Exception: If no H1 header is found.
    """
    lines = markdown.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            return line[2:]  # Return the text after '# '
    
    raise Exception("No H1 header found in the markdown content")