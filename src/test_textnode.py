import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("Different text", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.ANCHOR_TEXT, "https://example.com")
        node2 = TextNode("This is a text node", TextType.ANCHOR_TEXT, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.ANCHOR_TEXT, "https://example.com")
        node2 = TextNode("This is a text node", TextType.ANCHOR_TEXT, "https://example.com")
        self.assertEqual(node, node2)

    def test_eq_no_url(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_none_url_vs_url(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.ANCHOR_TEXT, "https://example.com")
        self.assertNotEqual(node,node2)
    def test_not_eq_different_class(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, "string")
        self.assertNotEqual(node, 123)

    def test_not_eq_different_text_type_and_url(self):
        node = TextNode("Test", TextType.NORMAL_TEXT, None)
        node2 = TextNode("Test", TextType.ANCHOR_TEXT, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_eq_none_url(self):
        node = TextNode("Test", TextType.NORMAL_TEXT, None)
        node2 = TextNode("Test", TextType.NORMAL_TEXT, None)
        self.assertEqual(node, node2)

    def test_not_eq_none_url_vs_different_none_url(self):
        node = TextNode("Test", TextType.NORMAL_TEXT, None)
        node2 = TextNode("Test2", TextType.NORMAL_TEXT, None)
        self.assertNotEqual(node, node2)