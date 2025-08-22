import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        nodeA = TextNode("node a, bold text", TextType.BOLD)
        nodeB = TextNode("node b, code text", TextType.CODE)
        self.assertNotEqual(nodeA, nodeB)

    def test_url_is_none(self):
        nodeA = TextNode("node a, bold text", TextType.BOLD, url=None)
        nodeB = TextNode("node b, code text", TextType.CODE)
        self.assertNotEqual(nodeA, nodeB)

    def test_almostEqual(self):
        nodeA = TextNode("node a, bold text", TextType.BOLD, "ayo")
        nodeB = TextNode("node a, bold text", TextType.BOLD)
        self.assertNotEqual(nodeA, nodeB)

    def test_idk_what_to_test(self):
        nodeA = TextNode("node a", TextType.ITALIC)
        nodeB = TextNode("node b ", TextType.ITALIC)
        self.assertNotEqual(nodeA, nodeB)

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_tth_link(self):
        node = TextNode("this is a link", TextType.LINK, "www.avalidlink.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this is a link")
        self.assertEqual(html_node.props, {"href": "www.avalidlink.com"})

    def test_tth_code(self):
        node = TextNode("this is a code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "this is a code snippet")

    def test_tth_wrong_text_type(self):
        node = TextNode("this text type is not supported", "underlined")

        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()