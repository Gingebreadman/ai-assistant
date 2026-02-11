import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        # Normalize working directory
        working_directory = os.path.abspath(working_directory)

        # Build full file path relative to working directory
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Validate path is inside working_directory
        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'

        # Check if full_path is a directory
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{full_path}" as it is a directory'

        # Ensure parent directories exist
        parent_dir = os.path.dirname(full_path)
        os.makedirs(parent_dir, exist_ok=True)

        # Write the file
        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the provided content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
