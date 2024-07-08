import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"class": "foo", "id": "bar"})
        expected_output = ' class="foo" id="bar"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_without_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_node_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello, World!", props={"class": "message"})
        expected_output = '<p class="message">Hello, World!</p>'
        self.assertEqual(node.to_html(), expected_output)

    def test_leaf_node_to_html_without_tag(self):
        node = LeafNode(value="Hello, World!")
        expected_output = "Hello, World!"
        self.assertEqual(node.to_html(), expected_output)

    def test_leaf_node_to_html_without_value(self):
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_single_leaf_node(self):
            node = LeafNode(tag="p", value="Hello, World!", props={"class": "message"})
            expected_output = '<p class="message">Hello, World!</p>'
            self.assertEqual(node.to_html(), expected_output)

    def test_single_parent_node_with_children(self):
        node = ParentNode(
            tag="div",
            children=[
                LeafNode(tag="p", value="Hello, World!"),
                LeafNode(tag="p", value="This is a paragraph."),
            ],
            props={"class": "container"},
        )
        expected_output = '<div class="container"><p>Hello, World!</p><p>This is a paragraph.</p></div>'
        self.assertEqual(node.to_html(), expected_output)

    def test_nested_parent_nodes(self):
        node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="section",
                    children=[
                        LeafNode(tag="h1", value="Header"),
                        LeafNode(tag="p", value="This is a paragraph."),
                    ],
                ),
                ParentNode(
                    tag="section",
                    children=[
                        LeafNode(tag="h2", value="Subheader"),
                        LeafNode(tag="p", value="Another paragraph."),
                    ],
                ),
            ],
            props={"class": "container"},
        )
        expected_output = '<div class="container"><section><h1>Header</h1><p>This is a paragraph.</p></section><section><h2>Subheader</h2><p>Another paragraph.</p></section></div>'
        self.assertEqual(node.to_html(), expected_output)

    def test_nested_multiple_levels(self):
        node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="section",
                    children=[
                        LeafNode(tag="h1", value="Header"),
                        ParentNode(
                            tag="div",
                            children=[
                                LeafNode(tag="p", value="Nested paragraph"),
                                ParentNode(
                                    tag="ul",
                                    children=[
                                        LeafNode(tag="li", value="Item 1"),
                                        LeafNode(tag="li", value="Item 2"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            props={"class": "container"},
        )
        expected_output = '<div class="container"><section><h1>Header</h1><div><p>Nested paragraph</p><ul><li>Item 1</li><li>Item 2</li></ul></div></section></div>'
        self.assertEqual(node.to_html(), expected_output)


if __name__ == "__main__":
    unittest.main()
