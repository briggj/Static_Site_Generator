import os
import markdown
import re

def markdown_to_html_node(markdown_text):
    """Converts markdown text to an HTML node.

    Args:
        markdown_text (str): The markdown text to convert.

    Returns:
        str: The HTML representation of the markdown text.
    """
    return markdown.markdown(markdown_text, extensions=['fenced_code', 'codehilite', 'tables'])

def extract_title(markdown_text):
    """Extracts the title from markdown text.

    Args:
        markdown_text (str): The markdown text to extract the title from.

    Returns:
        str: The extracted title, or "Untitled" if no title is found.
    """
    match = re.search(r'^#\s+(.+)', markdown_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"

def generate_page(from_path, template_path, dest_path):
    """Generates an HTML page from a markdown file using a template.

    Args:
        from_path (str): Path to the markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Path to save the generated HTML file.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print(f"Error: Markdown file not found at {from_path}")
        return

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        return

    html_content = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)

    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
    except Exception as e:
        print(f"Error writing to {dest_path}: {e}")
        return

    print(f"Successfully generated {dest_path}")
