import unittest
from block_markdown import ( 
    block_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_olist,
    block_type_ulist,
    block_type_quote,
    markdown_to_html_node,
    )    

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    
    def test_paragraph(self):
        block = "This is a paragraph."
        node = block_to_html_node(block)
        self.assertEqual(node.to_html(), '<p>This is a paragraph.</p>')
    
    def test_heading(self):
        block = "# Heading 1"
        node = block_to_html_node(block)
        self.assertEqual(node.to_html(), '<h1>Heading 1</h1>')

    def test_code(self):
        block = "```\nCode block\n```"
        node = block_to_html_node(block)
        self.assertEqual(node.to_html(), '<pre><code>Code block</code></pre>')
    
    def test_quote(self):
        block = "> This is a quote."
        node = block_to_html_node(block)
        self.assertEqual(node.to_html(), '<blockquote><p>This is a quote.</p></blockquote>')

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        node = block_to_html_node(block)
        self.assertEqual(node.to_html(), '<ul><li>Item 1</li><li>Item 2</li></ul>')

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        node = block_to_html_node(block)
        self.assertEqual(node.to_html(), '<ol><li>Item 1</li><li>Item 2</li></ol>')

    def test_full_document(self):
        markdown = """# Heading 1

        This is a paragraph.

        ```
        Code block
        ```

        > This is a quote.

        - Item 1
        - Item 2

        1. Item 1
        2. Item 2
        """
        node = markdown_to_html_node(markdown)
        expected_html = (
            '<div>'
            '<h1>Heading 1</h1>'
            '<p>This is a paragraph.</p>'
            '<pre><code>Code block</code></pre>'
            '<blockquote><p>This is a quote.</p></blockquote>'
            '<ul><li>Item 1</li><li>Item 2</li></ul>'
            '<ol><li>Item 1</li><li>Item 2</li></ol>'
            '</div>'
        )
        self.assertEqual(node.to_html().replace('\n', '').replace(' ', ''), expected_html.replace('\n', '').replace(' ', ''))

if __name__ == '__main__':
    unittest.main()
