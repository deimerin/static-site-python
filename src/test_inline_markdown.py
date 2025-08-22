import unittest
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType

class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "Hello, world!"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [TextNode("Hello, world!", TextType.TEXT)])


    def test_multiple_bold_segments(self):
        text = "This **is** very **bold**!"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This ", TextType.TEXT),
                TextNode("is", TextType.BOLD),
                TextNode(" very ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ]
        )

    def test_italic_text(self):
        text = "This is _italic_ text."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ]
        )

    def test_code_text(self):
        text = "Here is some `code`."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Here is some ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ]
        )

    def test_image(self):
        text = "Look at this ![alt text](image.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Look at this ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "image.png"),
            ]
        )

    def test_link(self):
        text = "Visit [Google](https://google.com) now."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" now.", TextType.TEXT),
            ]
        )

    def test_combined_styles(self):
        text = "Mix _italic_, **bold**, and `code`!"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("Mix ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("!", TextType.TEXT),
            ]
        )



