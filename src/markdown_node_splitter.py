# markdown_node_splitter.py
import re
from textnode import TextNode, TextType

def split_nodes_image(old_nodes):
    """Splits TextNode objects based on markdown image syntax."""
    new_nodes = []
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = []
            last_end = 0
            for match in re.finditer(image_pattern, node.text):
                start, end = match.span()
                if start > last_end:
                    parts.append((node.text[last_end:start], TextType.TEXT))
                parts.append((match.group(1), TextType.IMAGE, match.group(2)))
                last_end = end
            if last_end < len(node.text):
                parts.append((node.text[last_end:], TextType.TEXT))

            for part in parts:
                if len(part) == 2:
                    if part[1] == TextType.IMAGE:
                        new_nodes.append(TextNode(part[0], part[1], part[2], part[0]))
                    else:
                        new_nodes.append(TextNode(part[0], part[1]))
                elif len(part) == 3:
                    new_nodes.append(TextNode(part[0], part[1], part[2], part[0]))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    """Splits TextNode objects based on markdown link syntax."""
    new_nodes = []
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = []
            last_end = 0
            for match in re.finditer(link_pattern, node.text):
                start, end = match.span()
                if start > last_end:
                    parts.append((node.text[last_end:start], TextType.TEXT))
                parts.append((match.group(1), TextType.LINK, match.group(2)))
                last_end = end
            if last_end < len(node.text):
                parts.append((node.text[last_end:], TextType.TEXT))

            for part in parts:
                if len(part) == 2:
                    new_nodes.append(TextNode(part[0], part[1]))
                elif len(part) == 3:
                    new_nodes.append(TextNode(part[0], part[1], part[2]))

        else:
            new_nodes.append(node)
    return new_nodes