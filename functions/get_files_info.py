import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        dir_path = os.path.abspath(working_directory)
    else:
        dir_path = os.path.abspath(os.path.join(working_directory, directory))

    if (not dir_path.startswith(os.path.abspath(working_directory))
            or directory is not None and directory.startswith("..")):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = os.listdir(dir_path)
    except OSError as e:
        return f'Error: {e}'

    contents_string = ""
    try:
        for item in contents:
            contents_string += (f"{item}: "
                                f"file_size={os.path.getsize(os.path.join(dir_path, item))} bytes, "
                                f"is_dir={os.path.isdir(os.path.join(dir_path, item))}\n")
    except OSError as e:
        return f'Error: {e}'

    return contents_string