import unittest
from block_to_block_type import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Another paragraph with multiple lines.\nSecond line."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#Heading without space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### heading too many"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nMultiline code\nblock\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nSingle line code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nCode block"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Code block\n```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("````\ncode\n````"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> Quote line"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Quote line 1\n> Quote line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Quote line 1\nQuote line 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Quote line 1\n> Quote line 2"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\nItem 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Item 1\n- Item 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("* Item 1"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item A"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item A\n2. Item B"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item A\nItem B"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Item A\n2. Item B"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Item A\n3. Item c"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("0. Item A"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("a. Item A"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()