import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        # Normalize working directory
        working_directory = os.path.abspath(working_directory)

        # Build full file path relative to working directory
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Validate path is inside working_directory
        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check file exists and is a regular file
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check extension
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", full_path]
        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Build output string
        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
