# text_to_textnodes.py
import re
from textnode import TextNode, TextType # Assuming these are correctly defined

# --- Leaf Node Splitters (Image, Link) ---
# (Keep split_nodes_image and split_nodes_link as they were in the previous good version)
def split_nodes_image(old_nodes):
    # ... (same as previous version) ...
    new_nodes = []
    image_pattern = r"!\[([^\[\]]*)\]\(([^)]*?)\)"
    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node)
            continue
        original_text = node.text
        current_split_nodes = []
        last_end = 0
        processed_outer = False
        for match in re.finditer(image_pattern, original_text):
            processed_outer = True
            start, end = match.span()
            alt_text = match.group(1)
            url = match.group(2)
            if start > last_end:
                current_split_nodes.append(TextNode(original_text[last_end:start], TextType.TEXT))
            current_split_nodes.append(TextNode(alt_text, TextType.IMAGE, url, alt_text))
            last_end = end
        if last_end < len(original_text):
            current_split_nodes.append(TextNode(original_text[last_end:], TextType.TEXT))
        if processed_outer: new_nodes.extend(current_split_nodes)
        else: new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    # ... (same as previous version) ...
    new_nodes = []
    link_pattern = r"(?<!\!)\[([^\[\]]*)\]\(([^\)]*?)\)"
    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node)
            continue
        original_text = node.text
        current_split_nodes = []
        last_end = 0
        processed_outer = False
        for match in re.finditer(link_pattern, original_text):
            processed_outer = True
            start, end = match.span()
            anchor_text = match.group(1)
            url = match.group(2)
            if start > last_end:
                current_split_nodes.append(TextNode(original_text[last_end:start], TextType.TEXT))
            current_split_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            last_end = end
        if last_end < len(original_text):
            current_split_nodes.append(TextNode(original_text[last_end:], TextType.TEXT))
        if processed_outer: new_nodes.extend(current_split_nodes)
        else: new_nodes.append(node)
    return new_nodes


# --- Code Splitter ---
# Option A (Standard): Keep code blocks literal
def split_nodes_code(old_nodes):
    """Splits TEXT nodes around `code` segments. Content is treated literally."""
    new_nodes = []
    code_pattern = r"\`(.*?)\`"
    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node)
            continue

        original_text = node.text
        current_split_nodes = []
        last_end = 0
        processed_outer = False

        for match in re.finditer(code_pattern, original_text):
            processed_outer = True
            start, end = match.span()
            inner_content = match.group(1)
            # Add text before
            if start > last_end:
                current_split_nodes.append(TextNode(original_text[last_end:start], TextType.TEXT))
            # Add the code node with literal content
            current_split_nodes.append(TextNode(inner_content, TextType.CODE))
            last_end = end

        # Add text after
        if last_end < len(original_text):
            current_split_nodes.append(TextNode(original_text[last_end:], TextType.TEXT))

        # Add results to new_nodes
        if processed_outer:
            new_nodes.extend(current_split_nodes)
        else: # No matches in this node
            new_nodes.append(node)
    return new_nodes

# Option B (Non-standard): Parse images/links inside code blocks
# Uncomment this version and comment out Option A if you need this behavior
'''
def split_nodes_code(old_nodes):
    """Splits TEXT nodes around `code` segments. Parses images/links inside."""
    new_nodes = []
    code_pattern = r"\`(.*?)\`"
    # Patterns needed for inner parsing
    image_pattern = r"!\[([^\[\]]*)\]\(([^)]*?)\)"
    link_pattern = r"(?<!\!)\[([^\[\]]*)\]\(([^\)]*?)\)"

    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node); continue

        original_text = node.text
        current_split_nodes = []
        last_end = 0
        processed_outer = False

        for match in re.finditer(code_pattern, original_text):
            processed_outer = True
            start, end = match.span()
            inner_code_content = match.group(1)

            # 1. Add text before
            if start > last_end:
                current_split_nodes.append(TextNode(original_text[last_end:start], TextType.TEXT))

            # 2. Process inner code content for images and links
            temp_inner_nodes = []
            if inner_code_content:
                # Run image and link splitters on the inner content
                # Wrap inner content temporarily as a TEXT node for the splitters
                nodes_to_process = [TextNode(inner_code_content, TextType.TEXT)]
                split_nodes_inner = split_nodes_image(nodes_to_process)
                split_nodes_inner = split_nodes_link(split_nodes_inner) # Process result further

                # Now, re-type the resulting TEXT nodes as CODE nodes
                for inner_node in split_nodes_inner:
                    if inner_node.text_type == TextType.TEXT:
                        # Convert remaining text segments to CODE type
                        temp_inner_nodes.append(TextNode(inner_node.text, TextType.CODE, inner_node.url))
                    else:
                        # Keep IMAGE/LINK nodes as they are
                        temp_inner_nodes.append(inner_node)
            # If inner content was empty, temp_inner_nodes remains empty
            current_split_nodes.extend(temp_inner_nodes)
            # --- End Inner Processing ---
            last_end = end

        # 3. Add text after
        if last_end < len(original_text):
            current_split_nodes.append(TextNode(original_text[last_end:], TextType.TEXT))

        # Add results
        if processed_outer: new_nodes.extend(current_split_nodes)
        else: new_nodes.append(node)

    return new_nodes
'''

# --- Nestable Node Splitters (Bold, Italic) ---

def split_nodes_bold(old_nodes):
    """
    Splits TEXT nodes around **bold** segments.
    Processes inner content for _italic_ segments. (Fixes duplication bug)
    """
    new_nodes = []
    bold_pattern = r"\*\*(.*?)\*\*"
    italic_pattern = r"\_(.*?)\_"

    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node)
            continue

        original_text = node.text
        current_split_nodes = [] # Nodes generated from splitting *this* text node
        last_end = 0
        processed_outer = False # Flag if any bold match occurred in this node

        for match in re.finditer(bold_pattern, original_text):
            processed_outer = True
            start, end = match.span()
            inner_bold_content = match.group(1)

            # 1. Add text *before* the current match
            if start > last_end:
                current_split_nodes.append(TextNode(original_text[last_end:start], TextType.TEXT))

            # 2. Process the inner_bold_content for italics
            temp_inner_nodes = [] # Nodes generated ONLY from inner content
            inner_last_end = 0
            for inner_match in re.finditer(italic_pattern, inner_bold_content):
                inner_start, inner_end = inner_match.span()
                italic_content = inner_match.group(1)
                # Text before italic (as BOLD)
                if inner_start > inner_last_end:
                    temp_inner_nodes.append(TextNode(inner_bold_content[inner_last_end:inner_start], TextType.BOLD))
                # The ITALIC node
                temp_inner_nodes.append(TextNode(italic_content, TextType.ITALIC))
                inner_last_end = inner_end # Use inner_end here

            # Add remaining text after last italic (as BOLD)
            if inner_last_end < len(inner_bold_content):
                 temp_inner_nodes.append(TextNode(inner_bold_content[inner_last_end:], TextType.BOLD))

            # **Crucial Fix:** If temp_inner_nodes is empty ONLY THEN add the whole inner content as BOLD.
            # This prevents adding the plain bold node when inner italics *were* processed but covered the whole string.
            if not temp_inner_nodes and inner_bold_content:
                 temp_inner_nodes.append(TextNode(inner_bold_content, TextType.BOLD))

            current_split_nodes.extend(temp_inner_nodes) # Add nodes from inner processing

            last_end = end

        # 3. Add any remaining text *after* the last match
        if last_end < len(original_text):
            current_split_nodes.append(TextNode(original_text[last_end:], TextType.TEXT))

        # Decide what to add to the final list
        if processed_outer: # If we split this node
            new_nodes.extend(current_split_nodes)
        else: # If no matches were found in this node
            new_nodes.append(node) # Add original node back

    return new_nodes


def split_nodes_italic(old_nodes):
    """
    Splits remaining TEXT nodes around _italic_ segments.
    Assumes bold segments have already handled italics within them.
    """
    new_nodes = []
    italic_pattern = r"\_(.*?)\_"

    for node in old_nodes:
        if node.text_type != TextType.TEXT or not node.text:
            new_nodes.append(node)
            continue

        original_text = node.text
        current_split_nodes = []
        last_end = 0
        processed_outer = False

        for match in re.finditer(italic_pattern, original_text):
            processed_outer = True
            start, end = match.span()
            inner_content = match.group(1)
            # Add text before
            if start > last_end:
                current_split_nodes.append(TextNode(original_text[last_end:start], TextType.TEXT))
            # Add the italic node
            current_split_nodes.append(TextNode(inner_content, TextType.ITALIC))
            last_end = end

        # Add text after
        if last_end < len(original_text):
            current_split_nodes.append(TextNode(original_text[last_end:], TextType.TEXT))

        # Add results
        if processed_outer:
            new_nodes.extend(current_split_nodes)
        else: # No matches in this node
            new_nodes.append(node)
    return new_nodes

# --- Main Function ---

def text_to_textnodes(text):
    """
    Converts raw text to TextNodes, handling basic nesting.
    Uses standard Markdown rules (code blocks are literal by default).
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    initial_node = TextNode(text, TextType.TEXT)
    nodes = [initial_node]

    # Apply splitters - use Option A or B for split_nodes_code
    nodes = split_nodes_code(nodes) # Using Option A by default
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_bold(nodes) # Use revised bold splitter
    nodes = split_nodes_italic(nodes)

    # Filter out empty text nodes
    return [node for node in nodes if node.text is not None and node.text != ""]