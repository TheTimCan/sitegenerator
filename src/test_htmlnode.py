import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello world",
            None,
            {"class": "greeting", "href": "https://google.com"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://google.com"',
        )

    def test_leaf_node(self):
        node = LeafNode(
            "p",
            "This is a paragraph",
        )
        self.assertEqual(
            node.to_html(),
            '<p>This is a paragraph</p>'
        )

    def test_leaf_node2(self):
        node = LeafNode(
            "a",
            "Link",
            {"href": "https://google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com">Link</a>'
        )

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("i", "Italic text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b>Bold text</b><i>Italic text</i></p>'
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )




if __name__ == "__main__":
    unittest.main()
