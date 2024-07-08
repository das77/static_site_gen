import unittest
from textnode import TextNode
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


class TestInlineMarkdownFunctions(unittest.TestCase):

    def test_split_nodes_delimiter_single_node(self):
        node = TextNode("This is text with a `code block` word", "text")
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("This is text with a `code block` word", "text")
        node2 = TextNode("Another `code block` example", "text")
        expected_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
            TextNode("Another ", "text"),
            TextNode("code block", "code"),
            TextNode(" example", "text"),
        ]
        result = split_nodes_delimiter([node1, node2], "`", "code")
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimiter_no_text_nodes(self):
        node = TextNode("This is text with a `code block` word", "code")
        expected_nodes = [node]
        result = split_nodes_delimiter([node], "`", "text")
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimiter_empty_list(self):
        expected_nodes = []
        result = split_nodes_delimiter([], "`", "code")
        self.assertEqual(result, expected_nodes)


    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected_result = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), 
                           ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected_result)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected_result = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected_result)

    def test_extract_markdown_images_no_matches(self):
        text = "This is text without any images."
        expected_result = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected_result)

    def test_extract_markdown_links_no_matches(self):
        text = "This is text without any links."
        expected_result = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected_result)

    def test_extract_markdown_images_invalid_syntax(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_single_image(self):
        node = TextNode("This is text with an ![image](https://example.com/image.png)", "text")
        expected_output = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://example.com/image.png"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_multiple_images(self):
        node = TextNode(
            "Text before ![image1](https://example.com/image1.png) and more text ![image2](https://example.com/image2.png) after.",
            "text",
        )
        expected_output = [
            TextNode("Text before ", "text"),
            TextNode("image1", "image", "https://example.com/image1.png"),
            TextNode(" and more text ", "text"),
            TextNode("image2", "image", "https://example.com/image2.png"),
            TextNode(" after.", "text"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_no_image(self):
        node = TextNode("This is plain text with no image.", "text")
        expected_output = [
            TextNode("This is plain text with no image.", "text"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_edge_case_empty_text(self):
        node = TextNode("", "text")
        expected_output = [
            TextNode("", "text"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_edge_case_only_image(self):
        node = TextNode("![image](https://example.com/image.png)", "text")
        expected_output = [
            TextNode("image", "image", "https://example.com/image.png"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_text_only_before_image(self):
        node = TextNode("Text before ![image](https://example.com/image.png)", "text")
        expected_output = [
            TextNode("Text before ", "text"),
            TextNode("image", "image", "https://example.com/image.png"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_text_only_after_image(self):
        node = TextNode("![image](https://example.com/image.png) Text after", "text")
        expected_output = [
            TextNode("image", "image", "https://example.com/image.png"),
            TextNode(" Text after", "text"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_image_with_special_characters(self):
        node = TextNode("Text with ![special@image](https://example.com/special@image.png)", "text")
        expected_output = [
            TextNode("Text with ", "text"),
            TextNode("special@image", "image", "https://example.com/special@image.png"),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_output)

    def test_single_link(self):
        node = TextNode("This is text with a [link](https://example.com)", "text")
        expected_output = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://example.com"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_multiple_links(self):
        node = TextNode(
            "Here is a [link1](https://example1.com) and another [link2](https://example2.com) for you.",
            "text"
        )
        expected_output = [
            TextNode("Here is a ", "text"),
            TextNode("link1", "link", "https://example1.com"),
            TextNode(" and another ", "text"),
            TextNode("link2", "link", "https://example2.com"),
            TextNode(" for you.", "text")
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_no_link(self):
        node = TextNode("This is plain text with no link.", "text")
        expected_output = [
            TextNode("This is plain text with no link.", "text"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_edge_case_empty_text(self):
        node = TextNode("", "text")
        expected_output = [
            TextNode("", "text"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_edge_case_only_link(self):
        node = TextNode("[link](https://example.com)", "text")
        expected_output = [
            TextNode("link", "link", "https://example.com"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_link_at_start(self):
        node = TextNode("[link](https://example.com) followed by text.", "text")
        expected_output = [
            TextNode("link", "link", "https://example.com"),
            TextNode(" followed by text.", "text"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_link_at_end(self):
        node = TextNode("Text followed by a [link](https://example.com)", "text")
        expected_output = [
            TextNode("Text followed by a ", "text"),
            TextNode("link", "link", "https://example.com"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_link_with_special_characters(self):
        node = TextNode("Check [this@link](https://example.com/special?query=1&foo=bar)", "text")
        expected_output = [
            TextNode("Check ", "text"),
            TextNode("this@link", "link", "https://example.com/special?query=1&foo=bar"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

    def test_link_with_text_between(self):
        node = TextNode("First [link1](https://example1.com) middle [link2](https://example2.com) end.", "text")
        expected_output = [
            TextNode("First ", "text"),
            TextNode("link1", "link", "https://example1.com"),
            TextNode(" middle ", "text"),
            TextNode("link2", "link", "https://example2.com"),
            TextNode(" end.", "text"),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected_output)

def test_basic_text(self):
        text = "This is **bold** and *italic* with `code`."
        expected_output = [
            TextNode('This is ', 'text', None),
            TextNode('bold', 'bold', None),
            TextNode(' and ', 'text', None),
            TextNode('italic', 'italic', None),
            TextNode(' with ', 'text', None),
            TextNode('code', 'code', None),
            TextNode('.', 'text', None)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_output)

def test_text_with_image_and_link(self):
    text = "This is an ![image](https://example.com/image.png) and a [link](https://example.com)."
    expected_output = [
        TextNode('This is an ', 'text', None),
        TextNode('image', 'image', 'https://example.com/image.png'),
        TextNode(' and a ', 'text', None),
        TextNode('link', 'link', 'https://example.com'),
        TextNode('.', 'text', None)
    ]
    result = text_to_textnodes(text)
    self.assertEqual(result, expected_output)

def test_empty_text(self):
    text = ""
    expected_output = [
        TextNode('', 'text', None)
    ]
    result = text_to_textnodes(text)
    self.assertEqual(result, expected_output)

def test_text_with_edge_cases(self):
    text = "**bold without closing *italic missing backticks`"
    with self.assertRaises(ValueError):
        text_to_textnodes(text)

if __name__ == "__main__":
    unittest.main()