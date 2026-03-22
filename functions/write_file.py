import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites to a file in a specified directory relative to the working directory with a given filepath",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory filepath to write or overwrite a file to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written or overwritten to a file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs

    if not valid_target:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.split(target_file)[0], exist_ok=True)
        with open(target_file, "w") as f:
            num_written = f.write(content)
        if num_written > 0:
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return f'Error: Unable to open / write to {file_path}.'