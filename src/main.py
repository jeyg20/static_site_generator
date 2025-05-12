import os
import shutil

from src.markdown_parser import BlockType, block_to_block_type, format_heading, markdown_to_html_node


def copy_static_to_public_recursive(current_directory_path: str, static_base_dir: str, public_base_dir: str):
    if not os.path.isdir(current_directory_path):
        print(f"Error: {current_directory_path} is not a valid directory.")
        return

    try:
        with os.scandir(current_directory_path) as entries:
            for entry in entries:
                # Calculate the path relative to the static base directory
                relative_path_to_static = os.path.relpath(entry.path, static_base_dir)

                if entry.is_file():
                    # Construct the full destination path in the public directory
                    destination_file_path = os.path.join(public_base_dir, relative_path_to_static)
                    destination_parent_dir = os.path.dirname(destination_file_path)

                    # Create parent directories if they don't exist (safer with exist_ok=True)
                    if not os.path.exists(destination_parent_dir):
                        os.makedirs(destination_parent_dir, exist_ok=True)
                        print(f"Created directory: {destination_parent_dir}")

                    print(f"Copying: {entry.path} to {destination_file_path}")
                    shutil.copy(entry.path, destination_file_path)

                elif entry.is_dir():
                    copy_static_to_public_recursive(entry.path, static_base_dir, public_base_dir)

    except OSError as e:
        print(f"Error accessing directory {current_directory_path}: {e}")


def extract_title(first_line: str) -> str:
    """
    Extracts the title from the first line of markdown content.
    Assumes the title is the first block and must be a heading (h1-h6).

    Args:
        first_line: The string representing the first line of the markdown content.

    Returns:
        The extracted title string without markdown formatting.

    Raises:
        Exception: If the first line is not a valid heading block.
    """
    first_block_type = block_to_block_type(first_line)

    if first_block_type is BlockType.HEADING:
        heading_html_node = format_heading(first_line)
        title_text_parts = []
        for child_node in heading_html_node.children:
            if child_node.value is not None:
                title_text_parts.append(child_node.value)

        file_title = "".join(title_text_parts)

        return file_title.strip()

    raise Exception("The file does not contain a title heading (first line must be # ...)")


def generate_page(from_path, template_path, dest_path) -> None:
    """
    Generates a static HTML page from a markdown file using an HTML template.

    Reads markdown content from the `from_path`, extracts the title from the
    first line (assuming it's a heading), converts the markdown content to HTML
    nodes, and then renders the HTML content into a template read from
    `template_path`. The resulting populated HTML is written to the `dest_path`.

    Args:
        from_path (str): The full path to the source markdown file.
        template_path (str): The full path to the HTML template file.
                             The template is expected to contain '{{ Title }}'
                             and '{{ Content }}' placeholders.
        dest_path (str): The full path where the generated HTML file should be written.

    Returns:
        None: The function writes the output to `dest_path` and does not return a value.

    Raises:
        FileNotFoundError: If `from_path` or `template_path` do not exist.
        Exception: If the first line of the markdown file does not contain a title
                   (as determined by `extract_title`).
        # Add other potential exceptions from called functions if known and relevant
        # (e.g., errors from markdown parsing or file writing)
    """
    print(f"Generating page from {from_path} to {template_path} using {dest_path}")
    with open(from_path, "r", encoding="utf-8") as source_file:
        md_content = source_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()

    file_title = extract_title(md_content.splitlines(keepends=True)[0])
    html_content = markdown_to_html_node(md_content).to_html()

    populated_html = template_content.replace("{{ Title }}", file_title).replace("{{ Content }}", html_content)

    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(populated_html)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_base_dir = os.path.join(script_dir, "../content/index.md")
    template_dir = os.path.join(script_dir, "../content/template.html")
    static_base_dir = os.path.join(script_dir, "..", "static")
    public_base_dir = os.path.join(script_dir, "..", "public")

    # Clear the public directory before copying (optional, but common for SSGs)
    if os.path.exists(public_base_dir):
        print(f"Cleaning existing public directory: {public_base_dir}")
        shutil.rmtree(public_base_dir)
        os.makedirs(public_base_dir)

    # Ensure the public base directory exists
    os.makedirs(public_base_dir, exist_ok=True)
    print(f"Ensuring public directory exists: {public_base_dir}")

    # Start the recursive copy
    copy_static_to_public_recursive(static_base_dir, static_base_dir, public_base_dir)
    print("Static files copied to public.")

    basename = os.path.basename(md_base_dir)
    filename, ext = os.path.splitext(basename)
    generate_page(
        md_base_dir,
        template_dir,
        os.path.join(public_base_dir, filename + ".html"),
    )


if __name__ == "__main__":
    main()
