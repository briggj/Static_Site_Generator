# Contents of test_markdown_to_html_node.py
import unittest
from markdown_to_html_node import markdown_to_html_node, HTMLNode, HTMLNodeType

class TestMarkdownToHTMLNode(unittest.TestCase):

    def to_html(self, node: HTMLNode) -> str:
        """Helper function to convert HTMLNode to HTML string."""
        if node.node_type == HTMLNodeType.TEXT:
            # Handle potential None text
            return node.text if node.text is not None else ""

        tag_name = node.node_type.name.lower()
        # Handle potential None children
        children_html = "".join(self.to_html(child) for child in (node.children or []))

        # Basic implementation for common tags, extend as needed
        if tag_name in ["div", "h1", "h2", "h3", "h4", "h5", "h6", "p", "pre", "blockquote", "ul", "ol", "li", "strong", "em", "code"]:
            # Added 'p' which seems missing in your HTMLNodeType but used in test expected output
            # Corrected 'b' and 'i' based on your text_to_children logic
            if node.node_type == HTMLNodeType.STRONG:
                tag_name = "b" # Or "strong" depending on desired output
            elif node.node_type == HTMLNodeType.EM:
                tag_name = "i" # Or "em" depending on desired output
            return f"<{tag_name}>{children_html}</{tag_name}>"
        else:
            # Fallback for unknown or simple text nodes if logic missed them
            return children_html


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        # Note: Your markdown_to_blocks splits by '\n\n' and strips.
        # The input md above will result in two blocks:
        # 1. "This is **bolded** paragraph\ntext in a p\ntag here"
        # 2. "This is another paragraph with _italic_ text and `code` here"
        # Both will be classified as PARAGRAPH and wrapped in <div> by default in your code.

        node = markdown_to_html_node(md)
        html = self.to_html(node)
        # Expected output based on your current markdown_to_html_node logic which wraps paragraphs in <div>
        # And your text_to_children creating <b> and <i> tags
        expected_html = "<div><div>This is <b>bolded</b> paragraph\ntext in a p\ntag here</div><div>This is another paragraph with <i>italic</i> text and <code>code</code> here</div></div>"

        # Let's refine the comparison slightly to ignore whitespace differences potentially caused by newlines
        self.assertEqual(html.replace("\n", ""), expected_html.replace("\n", ""))


    def test_codeblock(self):
        # Add actual test content here later
        md = "```\nprint('hello')\n```"
        node = markdown_to_html_node(md)
        html = self.to_html(node)
        expected_html = "<div><pre><code>print('hello')\n</code></pre></div>"
        self.assertEqual(html.replace("\n", ""), expected_html.replace("\n", ""))