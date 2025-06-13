import logging
import os
import shutil
import sys

from src.header import generate_nav_bar
from src.markdown_parser import BlockType, block_to_block_type, format_heading, markdown_to_html_node

logger = logging.getLogger(__name__)


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


def generate_page(from_path: str, template_path: str, dest_path: str, basepath, content_directories: list[str]) -> None:
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

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.info("Generating page from %s to %s using %s", from_path, template_path, dest_path)
    with open(from_path, "r", encoding="utf-8") as source_file:
        md_content = source_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()

    if not md_content.strip():
        logger.warning(
            "Warning: Markdown file %s is empty or contains only whitespace. Skipping page generation.", from_path
        )
        return

    try:
        file_title = extract_title(md_content.splitlines(keepends=True)[0])
    except Exception as e:
        logger.exception(
            "Warning: Could not extract title from %s. Using default or handling failure. Error: %s", from_path, e
        )
        file_title = "Untitled Page"

    nav_html = generate_nav_bar(content_directories).to_html()
    html_content = markdown_to_html_node(md_content).to_html()

    populated_html = (
        template_content.replace("{{ Title }}", file_title)
        .replace("{{ nav }}", nav_html)
        .replace("{{ Content }}", html_content)
    )

    # **Perform the specified string replacements for base path**
    # This is the simplified and potentially brittle part as per the instructions.
    # Using an f-string to correctly insert the base_path variable value.
    populated_html = populated_html.replace('href="/', f'href="{basepath}')
    populated_html = populated_html.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(populated_html)


def process_content_directory(content_dir: str, template_path: str, output_dir: str, basepath):
    """
    Processes markdown files in a content directory and generates
    corresponding HTML pages in an output directory, mirroring the structure.

    Args:
        content_dir: The path to the source content directory.
        template_path: The path to the HTML template file.
        output_dir: The path to the output directory where generated HTML files will be written.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    if not os.path.isdir(content_dir):
        logger.exception("Error: Source is not a directory: %s", content_dir)
        return

    logger.info("Processing content from %s and generating pages in %s...", content_dir, output_dir)

    content_directories = [name for name in os.listdir(content_dir) if os.path.isdir(os.path.join(content_dir, name))]

    for root, _, files in os.walk(content_dir):
        relative_dir_path_from_content = os.path.relpath(root, content_dir)
        current_output_dir = os.path.join(output_dir, relative_dir_path_from_content)

        # Ensure the directory exists in the output path.
        try:
            os.makedirs(current_output_dir, exist_ok=True)
            logger.info("Created directory: %s", current_output_dir)
        except OSError as e:
            logger.error("Error ensuring outpu directory %s exists: %s", current_output_dir, e)

        for file in files:
            source_file_path = os.path.join(root, file)

            if file.endswith(".md"):
                file_relative_path_from_content = os.path.relpath(source_file_path, content_dir)
                output_file_basename = os.path.splitext(file_relative_path_from_content)[0] + ".html"
                output_file_path = os.path.join(output_dir, output_file_basename)

                try:
                    generate_page(source_file_path, template_path, output_file_path, basepath, content_directories)
                except Exception as e:
                    logger.exception("Error generating page from %s: %s", source_file_path, e)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    content_base_dir = os.path.normpath(os.path.join(script_dir, "..", "content"))
    template_path = os.path.normpath(os.path.join(script_dir, "..", "content", "template.html"))
    static_base_dir = os.path.normpath(os.path.join(script_dir, "..", "static"))
    public_base_dir = os.path.normpath(os.path.join(script_dir, "..", "docs"))

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        # Ensure the base path starts and ends with a slash for consistency
        if not basepath.startswith("/"):
            basepath = "/" + basepath
        if not basepath.endswith("/"):
            basepath += "/"

    logger.info(f"Using base path for generation: '{basepath}'")

    # Clean the public directory before copying
    if os.path.exists(public_base_dir):
        logger.info("Cleaning existing public directory: %s", public_base_dir)
        shutil.rmtree(public_base_dir)

    print(f"Ensuring public base directory exists: {public_base_dir}")
    os.makedirs(public_base_dir)

    # Copy static files to the public directory
    try:
        logger.info("Copying static files from %s to %s...", static_base_dir, public_base_dir)
        shutil.copytree(static_base_dir, public_base_dir, dirs_exist_ok=True)
        logger.info("Static files copied to public.")
    except FileNotFoundError:
        logger.error("Error: Static directory %s not found. Skipping static file copy.", static_base_dir)
    except Exception as e:
        logger.exception("An error occurred during static file copy: %s", e)

    # Call process_content_directory to generate pages in public
    try:
        process_content_directory(content_base_dir, template_path, public_base_dir, basepath)
        logger.info("Content processing and page generation complete.")
    except FileNotFoundError:
        logger.error("Error: Content directory %s not found. Skipping page generation.", content_base_dir)
    except Exception as e:
        logger.error("An error ocurred during content porcessing: %s", e)

    print("Static site generation complete.")


if __name__ == "__main__":
    main()
