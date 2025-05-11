import os
import shutil


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


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_base_dir = os.path.join(script_dir, "..", "static")
    public_base_dir = os.path.join(script_dir, "..", "public")

    # Clear the public directory before copying (optional, but common for SSGs)
    if os.path.exists(public_base_dir):
        print(f"Cleaning existing public directory: {public_base_dir}")
        shutil.rmtree(public_base_dir)

    # Ensure the public base directory exists
    os.makedirs(public_base_dir, exist_ok=True)
    print(f"Ensuring public directory exists: {public_base_dir}")

    # Start the recursive copy
    copy_static_to_public_recursive(static_base_dir, static_base_dir, public_base_dir)
    print("Static files copied to public.")


if __name__ == "__main__":
    main()
