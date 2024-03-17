import unittest

from textnode import TextNode
from main import main

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "https://example.com")
        node2 = TextNode("This is a text node", "bold", "https://example.com")
        self.assertEqual(node, node2)

    def test_different_text(self):
        node1 = TextNode("Hello", "header", "https://example.com")
        node2 = TextNode("World", "header", "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode("Hello", "header", "https://example.com")
        node2 = TextNode("Hello", "paragraph", "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_different_url(self):
        node1 = TextNode("Hello", "header", "https://example.com")
        node2 = TextNode("Hello", "header", "https://another-example.com")
        self.assertNotEqual(node1, node2)

    def test_none_url(self):
        node1 = TextNode("Hello", "header", "https://example.com")
        node2 = TextNode("Hello", "header", None)
        self.assertNotEqual(node1, node2)

    def test_none_text_type(self):
        node1 = TextNode("Hello", "header", "https://example.com")
        node2 = TextNode("Hello", None, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_none_url_and_text_type(self):
        node1 = TextNode("Hello", "header", "https://example.com")
        node2 = TextNode("Hello", None, None)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
