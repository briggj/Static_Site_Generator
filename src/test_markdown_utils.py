# test_markdown_utils.py
import unittest
from markdown_utils import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![image1](url1) and ![image2](url2)"
        )
        self.assertListEqual([("image1", "url1"), ("image2", "url2")], matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("This text has no images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![ ](url)")
        self.assertListEqual([(" ", "url")], matches)

    def test_extract_markdown_images_empty_url(self):
        matches = extract_markdown_images("![alt]( )")
        self.assertListEqual([("alt", " ")], matches)

    def test_extract_markdown_images_mixed_text(self):
        matches = extract_markdown_images("text ![alt](url) more text")
        self.assertListEqual([("alt", "url")], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links("[link1](url1) and [link2](url2)")
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("This text has no links.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_anchor(self):
        matches = extract_markdown_links("[ ](url)")
        self.assertListEqual([(" ", "url")], matches)

    def test_extract_markdown_links_empty_url(self):
        matches = extract_markdown_links("[anchor]( )")
        self.assertListEqual([("anchor", " ")], matches)

    def test_extract_markdown_links_mixed_text(self):
        matches = extract_markdown_links("text [anchor](url) more text")
        self.assertListEqual([("anchor", "url")], matches)

    def test_extract_markdown_links_and_images(self):
        text = "This has ![image](image.jpg) and [link](https://link.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://link.com")], link_matches)

    def test_nested_links(self):
        text = "This has a [nested [link](link.com)](outer_link.com)"
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("nested [link", "link.com")], link_matches)

    def test_escaped_brackets(self):
        text = "This has \\[escaped\\] brackets"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([], image_matches)
        self.assertListEqual([], link_matches)

if __name__ == "__main__":
    unittest.main()