import os
import shutil

def copy_recursive(source_dir_path: str, dest_dir_path: str):
    """
    Recursively copies files and directories from source_dir_path to dest_dir_path.

    Assumes dest_dir_path exists (or will be created for subdirectories).
    The initial clearing of the top-level destination should happen *before*
    calling this function for the first time.

    Args:
        source_dir_path: The path to the source directory.
        dest_dir_path: The path to the destination directory.
    """
    if not os.path.exists(source_dir_path):
        raise ValueError(f"Source directory not found: {source_dir_path}")
    if not os.path.isdir(source_dir_path):
         raise ValueError(f"Source path is not a directory: {source_dir_path}")
    if not os.path.exists(dest_dir_path):
        raise ValueError(f"Destination directory must exist before copying contents into it: {dest_dir_path}")


    print(f"Processing contents of: {source_dir_path}")

    for item_name in os.listdir(source_dir_path):
        source_item_path = os.path.join(source_dir_path, item_name)
        dest_item_path = os.path.join(dest_dir_path, item_name)

        if os.path.isfile(source_item_path):
            # If it's a file, copy it
            print(f"  Copying file: {source_item_path} -> {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)
        elif os.path.isdir(source_item_path):
            # If it's a directory, create the corresponding directory
            # in the destination and then recurse into it
            print(f"  Creating directory and entering: {dest_item_path}")
            # Create destination subdirectory (exist_ok=True handles potential race conditions)
            os.makedirs(dest_item_path, exist_ok=True)
            # Recursively call the function for the subdirectory
            copy_recursive(source_item_path, dest_item_path)
        else:
            print(f"  Skipping item (not file or dir): {source_item_path}")

# --- Main execution part ---
if __name__ == "__main__":
    # Define source and destination directories
    # In a real project, these might come from arguments or config files
    SOURCE_DIR = "static"
    DEST_DIR = "public"

    print(f"Starting copy process from '{SOURCE_DIR}' to '{DEST_DIR}'...")

    # 1. Validate Source Directory
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory '{SOURCE_DIR}' does not exist. Aborting.")
        exit(1) # Exit with an error code
    if not os.path.isdir(SOURCE_DIR):
         print(f"Error: Source path '{SOURCE_DIR}' is not a directory. Aborting.")
         exit(1)

    # 2. Clear Destination Directory
    if os.path.exists(DEST_DIR):
        print(f"Destination directory '{DEST_DIR}' exists. Clearing it first...")
        try:
            # shutil.rmtree removes the directory and all its contents
            shutil.rmtree(DEST_DIR)
            print(f"Successfully cleared '{DEST_DIR}'.")
        except OSError as e:
            print(f"Error clearing destination directory '{DEST_DIR}': {e}")
            exit(1) # Exit if clearing fails

    # 3. Recreate Destination Directory (ensures it exists even if source was empty)
    try:
        print(f"Creating empty destination directory '{DEST_DIR}'...")
        os.makedirs(DEST_DIR)
        print(f"Successfully created '{DEST_DIR}'.")
    except OSError as e:
        print(f"Error creating destination directory '{DEST_DIR}': {e}")
        exit(1) # Exit if creation fails

    # 4. Perform the Recursive Copy
    try:
        print("\nStarting recursive copy...")
        copy_recursive(SOURCE_DIR, DEST_DIR)
        print("\nCopy process completed successfully.")
    except Exception as e:
        print(f"\nAn error occurred during the copy process: {e}")
        exit(1)