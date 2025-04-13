import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_split(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_excessive_newlines(self):
        md = """
Block 1


Block 2



Block 3


"""
        expected = [
            "Block 1",
            "Block 2",
            "Block 3",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_leading_trailing_whitespace_blocks(self):
        md = """
   Block 1 has leading/trailing spaces   

  \t Block 2 has tabs \t

 Block 3 is normal

"""
        expected = [
            "Block 1 has leading/trailing spaces",
            "Block 2 has tabs",
            "Block 3 is normal",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_leading_trailing_whitespace_document(self):
        md = """

  Leading whitespace block before content

Content Block 1

Content Block 2

  Trailing whitespace block after content   

"""
        expected = [
            "Leading whitespace block before content",
            "Content Block 1",
            "Content Block 2",
            "Trailing whitespace block after content",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_blocks_with_only_whitespace(self):
        md = "Block 1\n\n   \t   \n\nBlock 2\n\n \n \n\nBlock3"
        expected = [
            "Block 1",
            "Block 2",
            "Block3",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_no_double_newlines(self):
        md = "This is just one block.\nIt might have single newlines.\n   And leading/trailing spaces.   "
        expected = [
            "This is just one block.\nIt might have single newlines.\n   And leading/trailing spaces."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

        md_single_line = "Single line block"
        self.assertEqual(markdown_to_blocks(md_single_line), ["Single line block"])

    def test_empty_and_whitespace_string_input(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("   "), [])
        self.assertEqual(markdown_to_blocks("\n\n"), [])
        self.assertEqual(markdown_to_blocks("  \n\n  "), [])
        self.assertEqual(markdown_to_blocks("\n\n\n\n"), [])

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            markdown_to_blocks(None)
        with self.assertRaises(TypeError):
            markdown_to_blocks(12345)
        with self.assertRaises(TypeError):
            markdown_to_blocks(["list", "of", "strings"])

if __name__ == "__main__":
    unittest.main()