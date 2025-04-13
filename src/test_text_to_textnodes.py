import unittest
from text_to_textnodes import text_to_textnodes  # Correct import
from textnode import TextNode, TextType

class TestTextToTextNodes(unittest.TestCase):

    def test_basic_text(self):
        text = "This is basic text."
        expected = [TextNode("This is basic text.", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_text(self):
        text = "This is _italic_ text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_text(self):
        text = "This is `code` text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image_text(self):
        text = "This is ![image](url) text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url", "image"),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link_text(self):
        text = "This is [link](url) text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_mixed_text(self):
        text = "This is **bold** and _italic_ and `code` and ![image](url) and [link](url) text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url","image"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_complex_mixed_text(self):
        text = "This is **bold _italic_ bold** and `code ![image](url) code` [link](url) text."
        #   ADJUSTED EXPECTED OUTPUT: Code block content is literal
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold ", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode(" bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code ![image](url) code", TextType.CODE), # Changed this line
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_alt_image(self):
        text = "![ ](url)"
        expected = [TextNode(" ", TextType.IMAGE, "url", " ")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_url_image(self):
        text = "![alt]( )"
        expected = [TextNode("alt", TextType.IMAGE, " ", "alt")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_anchor_link(self):
        text = "[ ](url)"
        expected = [TextNode(" ", TextType.LINK, "url")]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_empty_url_link(self):
        text = "[anchor]( )"
        expected = [TextNode("anchor", TextType.LINK, " ")]
        self.assertEqual(text_to_textnodes(text), expected)