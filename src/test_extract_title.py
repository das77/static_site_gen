import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_valid_h1_header(self):
        markdown_content = "# Example Title\nSome content here.\n## Subheader\nMore content here."
        self.assertEqual(extract_title(markdown_content), "Example Title")
    
    def test_valid_h1_header_with_extra_spaces(self):
        markdown_content = "#    Example Title\nSome content here.\n## Subheader\nMore content here."
        self.assertEqual(extract_title(markdown_content), "   Example Title")
    
    def test_no_h1_header(self):
        markdown_content = "## Subheader\nMore content here."
        with self.assertRaises(Exception) as context:
            extract_title(markdown_content)
        self.assertTrue("No H1 header found in the markdown content" in str(context.exception))
    
    def test_empty_markdown(self):
        markdown_content = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown_content)
        self.assertTrue("No H1 header found in the markdown content" in str(context.exception))
    
    def test_multiple_h1_headers(self):
        markdown_content = "# First Title\n# Second Title"
        self.assertEqual(extract_title(markdown_content), "First Title")
    
    def test_h1_header_with_hash_in_text(self):
        markdown_content = "# Example # Title\nSome content here.\n## Subheader\nMore content here."
        self.assertEqual(extract_title(markdown_content), "Example # Title")

if __name__ == '__main__':
    unittest.main()
