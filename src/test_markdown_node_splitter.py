# test_markdown_node_splitter.py
import unittest
from markdown_node_splitter import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestMarkdownNodeSplitter(unittest.TestCase):

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png", "image"),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png", "image"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png", "second image"),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode("This is text with no image.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_image_at_start(self):
        node = TextNode("![image](url) text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url", "image"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode("text ![image](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url", "image"),
            ],
            new_nodes,
        )

    def test_split_images_consecutive_images(self):
        node = TextNode("![image1](url1)![image2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "url1", "image1"),
                TextNode("image2", TextType.IMAGE, "url2", "image2"),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt(self):
        node = TextNode("![ ](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode(" ", TextType.IMAGE, "url", " ")], new_nodes)

    def test_split_images_empty_url(self):
        node = TextNode("![alt]( )", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("alt", TextType.IMAGE, " ", "alt")], new_nodes)

    def test_split_links_single(self):
        node = TextNode("This is text with a [link](https://www.example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode("This text has [link1](url1) and [link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode("This text has no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_link_at_start(self):
        node = TextNode("[link](url) text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode("text [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive_links(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_empty_anchor(self):
        node = TextNode("[ ](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode(" ", TextType.LINK, "url")], new_nodes)

    def test_split_links_empty_url(self):
        node = TextNode("[anchor]( )", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("anchor", TextType.LINK, " ")], new_nodes)

    def test_split_links_and_images(self):
        node = TextNode("text ![image](img_url) text [link](link_url) text", TextType.TEXT)
        new_nodes = split_nodes_link(split_nodes_image([node])) # correct order
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img_url", "image"),
                TextNode(" text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "link_url"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )