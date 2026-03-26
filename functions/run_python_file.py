import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.realpath(working_directory)
    target_file = os.path.realpath(os.path.join(working_dir_abs, file_path))
    if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
        return (f'Error: Cannot execute "{file_path}" as it is outside '
                f'the permitted working directory')
    elif not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmd = ["python3", target_file]
        if args:
            cmd.extend(args)
        output = subprocess.run(cmd,
                                capture_output=True,
                                cwd=os.path.realpath(working_directory),
                                timeout=30)
        stdout = output.stdout.decode("utf-8")
        stderr = output.stderr.decode("utf-8")
        result = f'STDOUT: {stdout}\nSTDERR: {stderr}'
        if output.returncode != 0:
            result += f'\nProcess exited with code {output.returncode}'
        if len(stdout) == 0 and len(stderr) == 0 and output.returncode == 0:
            return 'No output produced.'
        return result
    except (subprocess.TimeoutExpired, Exception) as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file and returns its output. The file must be within the working directory and have a .py extension.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to target file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional array of arguments to pass to the execution of the target file",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Individual argument to pass to the execution of the target file",
                ),

            ),
        },
    ),
)
