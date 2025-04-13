from typing import List

def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Splits a raw Markdown string into a list of block strings.

    Blocks are separated by double newlines. Leading/trailing whitespace
    is stripped from each block, and empty blocks (resulting from
    multiple double newlines or whitespace) are removed.
    """
    if not isinstance(markdown, str):
        raise TypeError("Input must be a string")

    blocks = markdown.split('\n\n')

    processed_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            processed_blocks.append(stripped_block)

    return processed_blocks