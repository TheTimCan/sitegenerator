import unittest

from textnode import (
        TextNode, 
        split_nodes_delimiter,
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_split_delimiter(self):
        node = TextNode("This is text with a **bold* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ]
        )



if __name__ == "__main__":
    unittest.main()
