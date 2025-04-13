# node_splitter.py
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TextNode objects based on a delimiter and applies a specified TextType.

    Args:
        old_nodes (list): A list of TextNode objects to split.
        delimiter (str): The delimiter to use for splitting the text.
        text_type (TextType): The TextType to apply to the split parts.

    Returns:
        list: A list of new TextNode objects.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 1:
                    new_nodes.append(TextNode(part, text_type))
                elif part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes