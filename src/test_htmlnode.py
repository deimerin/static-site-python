import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TextHTMLNode(unittest.TestCase):
    def test_None_Defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_NotImplementedError(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_Props_To_HTML(self):
        expected_string = 'href="https://www.google.com" target="_blank"'
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(expected_string, node.props_to_html())

    # Leaf Nodes

    def test_leaf_node_children(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertIsNone(node.children)

    def test_leaf_node_to_html(self):
        expected_string = '<a href="https://www.google.com">Click me!</a>'
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(expected_string, node.to_html())

    # I should probably write some more test here
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",
    )


if __name__ == '__main__':
    unittest.main()