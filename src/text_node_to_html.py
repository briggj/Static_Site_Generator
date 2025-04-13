# text_node_to_html.py
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    """
    Converts a TextNode object to an HTMLNode object.

    Args:
        text_node (TextNode): The TextNode object to convert.

    Returns:
        HTMLNode: The corresponding HTMLNode object.
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url or not text_node.alt:
            raise ValueError("Image TextNode requires both url and alt attributes.")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.alt})
    else:
        raise ValueError(f"Unknown TextType: {text_node.text_type}")