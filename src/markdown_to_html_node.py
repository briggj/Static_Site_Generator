import enum
from typing import List, Union

class HTMLNodeType(enum.Enum):
    TEXT = 1
    EM = 2
    STRONG = 3
    CODE = 4
    DIV = 5
    H1 = 6
    H2 = 7
    H3 = 8
    H4 = 9
    H5 = 10
    H6 = 11
    PRE = 12
    BLOCKQUOTE = 13
    UL = 14
    OL = 15
    LI = 16

class HTMLNode:
    def __init__(self, node_type: HTMLNodeType, children: List['HTMLNode'] = None, text: str = None):
        self.node_type = node_type
        self.children = children or []
        self.text = text

def markdown_to_blocks(markdown: str) -> List[str]:
    if not isinstance(markdown, str):
        raise TypeError("Input must be a string")
    blocks = markdown.split('\n\n')
    processed_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            processed_blocks.append(stripped_block)
    return processed_blocks

class BlockType(enum.Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()
    if not lines:
        return BlockType.PARAGRAPH
    if lines[0].startswith('#'):
        if lines[0].startswith('###### '):
          return BlockType.HEADING
        elif lines[0].startswith('##### '):
          return BlockType.HEADING
        elif lines[0].startswith('#### '):
          return BlockType.HEADING
        elif lines[0].startswith('### '):
          return BlockType.HEADING
        elif lines[0].startswith('## '):
          return BlockType.HEADING
        elif lines[0].startswith('# '):
          return BlockType.HEADING
        else:
          return BlockType.PARAGRAPH
    if block.startswith('```'):
        if block.endswith('```'):
            if block.count('```') == 2:
                if block.count('\n') == 0 or block.startswith('```\n') or block.endswith('\n```'):
                    return BlockType.CODE
                else:
                    return BlockType.PARAGRAPH
            else:
                return BlockType.PARAGRAPH
        else:
            return BlockType.PARAGRAPH
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f'{i+1}. ') for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_node_to_html_node(text_node: str) -> HTMLNode:
    return HTMLNode(HTMLNodeType.TEXT, text=text_node)

def text_to_children(text: str) -> List[HTMLNode]:
        children = []
        i = 0
        while i < len(text):
            # Check for **bold**
            if text[i:i+2] == '**':
                end = text.find('**', i + 2)
                if end != -1:
                    content = text[i+2:end]
                    children.append(HTMLNode(HTMLNodeType.STRONG, children=text_to_children(content)))
                    i = end + 2
                    continue

            # Check for _italic_ (Corrected condition)
            elif text[i:i+1] == '_': # Check the single character at index i
                end = text.find('_', i + 1) # Find the *next* single underscore
                if end != -1:
                    content = text[i+1:end] # Content is between i+1 and end
                    children.append(HTMLNode(HTMLNodeType.EM, children=text_to_children(content)))
                    i = end + 1 # Move index past the closing underscore
                    continue

            # Check for `code`
            elif text[i:i+1] == '`':
                end = text.find('`', i + 1)
                if end != -1:
                    content = text[i+1:end]
                    # Code content is usually literal text, no recursive call needed
                    children.append(HTMLNode(HTMLNodeType.CODE, children=[text_node_to_html_node(content)]))
                    i = end + 1
                    continue

            # If no delimiter matched, append the current character as a text node
            children.append(text_node_to_html_node(text[i]))
            i += 1 # Move to the next character

        return children

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode(HTMLNodeType.DIV)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            parent_node.children.append(HTMLNode(HTMLNodeType.DIV, children=text_to_children(block)))
        elif block_type == BlockType.HEADING:
            level = block.count('#', 0, block.find(' '))
            if level == 1:
                parent_node.children.append(HTMLNode(HTMLNodeType.H1, children=text_to_children(block[block.find(' ')+1:])))
            elif level == 2:
                parent_node.children.append(HTMLNode(HTMLNodeType.H2, children=text_to_children(block[block.find(' ')+1:])))
            elif level == 3:
                parent_node.children.append(HTMLNode(HTMLNodeType.H3, children=text_to_children(block[block.find(' ')+1:])))
            elif level == 4:
                parent_node.children.append(HTMLNode(HTMLNodeType.H4, children=text_to_children(block[block.find(' ')+1:])))
            elif level == 5:
                parent_node.children.append(HTMLNode(HTMLNodeType.H5, children=text_to_children(block[block.find(' ')+1:])))
            elif level == 6:
                parent_node.children.append(HTMLNode(HTMLNodeType.H6, children=text_to_children(block[block.find(' ')+1:])))
        elif block_type == BlockType.CODE:
            parent_node.children.append(HTMLNode(HTMLNodeType.PRE, children=[HTMLNode(HTMLNodeType.CODE, children=[text_node_to_html_node(block[3:-3] if block.endswith('```') else block[3:])])]))
        elif block_type == BlockType.QUOTE:
            parent_node.children.append(HTMLNode(HTMLNodeType.BLOCKQUOTE, children=text_to_children('\n'.join([line[2:] for line in block.splitlines()]))))
        elif block_type == BlockType.UNORDERED_LIST:
            list_node = HTMLNode(HTMLNodeType.UL)
            for line in block.splitlines():
                list_node.children.append(HTMLNode(HTMLNodeType.LI, children=text_to_children(line[2:])))
            parent_node.children.append(list_node)
        elif block_type == BlockType.ORDERED_LIST:
            list_node = HTMLNode(HTMLNodeType.OL)
            for line in block.splitlines():
                list_node.children.append(HTMLNode(HTMLNodeType.LI, children=text_to_children(line[line.find('.')+2:])))
            parent_node.children.append(list_node)
    return parent_node