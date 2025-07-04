import os
import subprocess

def run_python_file(working_directory, file_path):
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(absolute_file_path):
        return f'Error: File "{file_path}" not found.'
    elif not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    else:
        try:
            output = subprocess.run(['python3', absolute_file_path],
                                    capture_output=True, cwd=os.path.abspath(working_directory), timeout=30)

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
