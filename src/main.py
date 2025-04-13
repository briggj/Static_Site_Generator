import os
import shutil
from pathlib import Path
import markdown
import re

# Assuming textnode.py is in the same directory as main.py or accessible
from textnode import TextNode, TextType

# --- Function Definitions ---

def extract_title(markdown: str) -> str:
    """Extracts the title from markdown text.

    Args:
        markdown (str): The markdown text to extract the title from.

    Returns:
        str: The extracted title, or raises ValueError if no title is found.
    """
    if not isinstance(markdown, str):
        raise TypeError("Input 'markdown' must be a string.")

    lines = markdown.splitlines()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            title = stripped_line[2:].strip()
            return title

    raise ValueError("No H1 header found in the Markdown document.")


def copy_recursive(source_dir_path: str, dest_dir_path: str):
    """Recursively copies files and directories from source to destination.

    Args:
        source_dir_path (str): Path to the source directory.
        dest_dir_path (str): Path to the destination directory.
    """
    print(f"Processing contents of: {source_dir_path}")

    for item_name in os.listdir(source_dir_path):
        source_item_path = os.path.join(source_dir_path, item_name)
        dest_item_path = os.path.join(dest_dir_path, item_name)

        if os.path.isfile(source_item_path):
            print(f"  Copying file: {source_item_path} -> {dest_item_path}")
            shutil.copy2(source_item_path, dest_item_path)  # Use copy2 to preserve metadata
        elif os.path.isdir(source_item_path):
            print(f"  Creating directory and entering: {dest_item_path}")
            os.makedirs(dest_item_path, exist_ok=True)
            copy_recursive(source_item_path, dest_item_path)
        else:
            print(f"  Skipping item (not file or dir): {source_item_path}")


def markdown_to_html_node(markdown_text: str) -> str:
    """Converts markdown text to an HTML string.

    Args:
        markdown_text (str): The markdown text to convert.

    Returns:
        str: The HTML representation of the markdown text.
    """
    return markdown.markdown(markdown_text, extensions=['fenced_code', 'codehilite', 'tables'])



def generate_page(from_path: str, template_path: str, dest_path: str):
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
    try:
        title = extract_title(markdown_content)
    except ValueError:
        title = "Untitled"  # Or some other default title

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



def main():
    """Main function to generate the website."""
    # NOTE: Original TextNode example kept from your code
    print("Original TextNode example:")
    node = TextNode("Example Text", TextType.LINK, "https://example.com")
    print(node)
    print("-" * 30)

    # --- Configuration ---
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.dirname(current_script_dir)
    source_dir = os.path.join(project_root_dir, "static")
    dest_dir = os.path.join(project_root_dir, "public")
    content_dir = os.path.join(project_root_dir, "content")  # Added content directory
    template_file = "template.html"  #  Added template file name
    index_file = "index.md" # Added index file name

    # --- Preparation ---
    print("Starting static directory copy process...")
    print(f"Calculated source directory: {source_dir}")
    print(f"Calculated destination directory: {dest_dir}")

    print(f"Validating source: '{source_dir}'")
    if not os.path.exists(source_dir):
        print(f"❌ Error: Source directory '{source_dir}' does not exist. Aborting copy.")
        return
    if not os.path.isdir(source_dir):
        print(f"❌ Error: Source path '{source_dir}' is not a directory. Aborting copy.")
        return
    print("✅ Source directory validated.")

    print(f"Preparing destination: '{dest_dir}'")
    if os.path.exists(dest_dir):
        print(f"  Destination '{dest_dir}' exists. Clearing it first...")
        try:
            shutil.rmtree(dest_dir)
            print(f"  Successfully cleared '{dest_dir}'.")
        except OSError as e:
            print(f"❌ Error clearing destination directory '{dest_dir}': {e}")
            return

    try:
        print(f"  Creating empty destination directory '{dest_dir}'...")
        os.makedirs(dest_dir)
        print(f"  Successfully created '{dest_dir}'.")
    except OSError as e:
        print(f"❌ Error creating destination directory '{dest_dir}': {e}")
        return

    # --- Copy Static Files ---
    try:
        print("\n🚀 Starting recursive copy...")
        copy_recursive(source_dir, dest_dir)
        print("\n✅ Copy process completed successfully.")
    except Exception as e:
        print(f"\n❌ An error occurred during the copy process: {e}")
        return  # Important: Exit if copying fails

    # --- Generate index.html ---
    print("\nGenerating index.html...")
    generate_page(
        from_path=os.path.join(content_dir, index_file),  # Use os.path.join
        template_path=template_file,
        dest_path=os.path.join(dest_dir, "index.html"),  #  Use os.path.join
    )
    print("Finished generating index.html")

    print("-" * 30)
    print("Script finished.")



# --- Main Execution ---

if __name__ == "__main__":
    # This single block now calls the main function directly
    main()
