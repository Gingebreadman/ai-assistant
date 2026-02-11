import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        # Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build the target directory path safely
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Ensure the target directory is inside the working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure the target path is actually a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # List directory contents
        items = []
        for name in os.listdir(target_dir):
            item_path = os.path.join(target_dir, name)
            is_dir = os.path.isdir(item_path)

            # Directories have size = size of directory entry (OS-dependent)
            try:
                size = os.path.getsize(item_path)
            except Exception:
                size = 0  # fallback if OS blocks size lookup

            items.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(items)

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
