import os

from google.genai import types


def get_files_info(working_directory, directory='.'):
    working_dir_abs = os.path.realpath(working_directory)
    target_dir = os.path.realpath(os.path.join(working_dir_abs, directory))
    if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
        return (f'Error: Cannot list "{directory}" as it is outside '
                f'the permitted working directory')
    elif not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = os.listdir(target_dir)
    except OSError as e:
        return f'Error: {e}'
    contents_string = ""
    try:
        for item in contents:
            contents_string += (f"- {item}: "
                                f"file_size={os.path.getsize(
                                    os.path.join(target_dir, item))} bytes, "
                                f"is_dir={os.path.isdir(
                                    os.path.join(target_dir, item))}\n")
    except OSError as e:
        return f'Error: {e}'
    return contents_string


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
