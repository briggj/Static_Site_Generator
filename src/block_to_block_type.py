import enum
from typing import List

class BlockType(enum.Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block: str) -> BlockType:
    """
    Determines the BlockType of a given markdown block.

    Args:
        block: A single block of markdown text (leading/trailing whitespace stripped).

    Returns:
        The BlockType representing the type of the block.
    """

    lines = block.splitlines()

    # Handle empty block
    if not lines:
        return BlockType.PARAGRAPH

    # Heading
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

    # Code
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

    # Quote
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    if all(line.startswith(f'{i+1}. ') for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # Paragraph
    return BlockType.PARAGRAPH