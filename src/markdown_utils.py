import re

def extract_markdown_images(text):
    """
    Extracts markdown image URLs and alt text from a given string.

    Args:
        text (str): The markdown text to extract images from.

    Returns:
        list: A list of tuples, where each tuple contains (alt_text, url).
    """
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown link URLs and link text from a given string.

    Args:
        text (str): The markdown text to extract links from.

    Returns:
        list: A list of tuples, where each tuple contains (link_text, url).
    """
    link_pattern = r"(?<!!)\[(.*?)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches