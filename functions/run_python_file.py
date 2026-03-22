import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a program file in a specified directory relative to the working directory with a given filepath",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory filepath to execute a python file from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass into a function called from executing a python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arguments passed into the function called from executing a python file."
                ),
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
    
    if not valid_target:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if target_file[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        completed = subprocess.run(command, cwd=working_directory_abs, capture_output=True, timeout=30, text=True)

        output = ""

        if completed.returncode != 0:
            output += f"Process exited with code {completed.returncode}\n"
        
        output += "STDOUT: "
        if not completed.stdout:
            output += "No output produced\n"
        else:
            output += completed.stdout + "\n"

        output += "STDERR: "
        if not completed.stderr:
            output += "No output produced\n"
        else:
            output += completed.stderr

        return output

    except Exception as e:
        f"Error: executing Python file: {e}"
