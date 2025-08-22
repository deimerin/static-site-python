import unittest

from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    #
    # I got lazy and let copilot write these
    # 
    def test_no_delimiter(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("Hello world", TextType.TEXT)])

    def test_single_delimiter_pair(self):
        nodes = [TextNode("Hello **world**!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiter_pairs(self):
        nodes = [TextNode("**Hello** and **world**!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Hello", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises(self):
        nodes = [TextNode("Hello **world!", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_non_text_nodes_untouched(self):
        node = TextNode("img.png", TextType.IMAGE)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [])

    # holy shit copilot is bad
    def test_raises_exception_on_odd_number_of_delimiters(self):
        nodes = [TextNode("This **should** fail** here", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # more copilot slop
    def test_split_nodes_image_single_image(self):
        nodes = [TextNode("This is an ![alt](img.png) image.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "img.png"),
            TextNode(" image.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_images(self):
        nodes = [TextNode("![a](1.png) and ![b](2.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("a", TextType.IMAGE, "1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "2.png"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_image(self):
        nodes = [TextNode("No images here.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [TextNode("No images here.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_image_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [])

    def test_split_nodes_link_single_link(self):
        nodes = [TextNode("Click [here](http://a.com) please.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "http://a.com"),
            TextNode(" please.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple_links(self):
        nodes = [TextNode("[A](a.com) and [B](b.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("A", TextType.LINK, "a.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("B", TextType.LINK, "b.com"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_link(self):
        nodes = [TextNode("No links here.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("No links here.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_link_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [])

    ## Debug test
    def test_simple_bold_debug(self):
        node = TextNode("**bold**", TextType.TEXT)            
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        #print("Input:", node)
        #print("Result:", result)
        #print("Expected: [TextNode('bold', TextType.BOLD)]")
